#!/usr/bin/env python3
"""
Classify grants by exposure type across all disease areas.
"""

import pandas as pd
import re
import os
from pathlib import Path

# Define exposure categories and their keywords
EXPOSURE_PATTERNS = {
    'Microbiome': [
        r'\bmicrobiome\b', r'\bmicrobiota\b', r'\bgut.?brain\b', r'\bgut.?liver\b',
        r'\bintestinal\s+flora\b', r'\bcommensal\b', r'\bdysbiosis\b', r'\bprobiotic\b',
        r'\bprebiotic\b', r'\bfecal\s+transplant\b', r'\bFMT\b', r'\bbacterial\s+colonization\b',
        r'\bgut\s+bacteria\b', r'\bintestinal\s+microb', r'\boral\s+microb', r'\bvaginal\s+microb',
        r'\bskin\s+microb', r'\blung\s+microb', r'\brespiratory\s+microb',
        r'\b16S\s+rRNA\b', r'\bmetagenom', r'\benterotype', r'\blactobacillus\b',
        r'\bbifidobacter', r'\bfirmicutes\b', r'\bbacteroidetes\b', r'\bakkermansia\b',
        r'\bfusobacterium\b', r'\bhelicobacter\b', r'\benterococcus\b', r'\bclostridium\b',
        r'\benterobacter', r'\bshort.?chain\s+fatty\s+acid', r'\bSCFA\b', r'\bbutyrate\b',
    ],

    'Smoking': [
        r'\bsmok', r'\btobacco\b', r'\bcigarette\b', r'\bnicotine\b', r'\bvap(?:e|ing)\b',
        r'\be.?cigarette', r'\bnicotinic\b', r'\bcotinine\b', r'\bsnuff\b', r'\bsmoker\b',
        r'\bcessation\b.*(?:smok|tobacco)', r'\btobacco.*cessation', r'\blung\s+carcinogen',
        r'\bNNK\b', r'\bNNN\b', r'\bbenzo\[a\]pyrene\b', r'\bpolycyclic\s+aromatic',
        r'\bPAH\b', r'\bsecondhand\s+smoke\b', r'\bpassive\s+smok', r'\bthirdhand\b',
    ],

    'Alcohol': [
        r'\balcohol', r'\bethanol\b', r'\bdrinking\b', r'\bbinge\s+drink', r'\bAUD\b',
        r'\balcohol\s+use\s+disorder', r'\balcoholic\b', r'\bcirrhosis\b', r'\bASH\b',
        r'\balcohol.?related', r'\bALD\b', r'\balcohol.?induced', r'\bFAS\b', r'\bFASD\b',
        r'\bfetal\s+alcohol', r'\bacetaldehyde\b', r'\bADH\b.*alcohol', r'\bALDH\b',
        r'\bCYP2E1\b', r'\bliver\s+fibrosis\b', r'\bhepatic\s+steatosis\b',
    ],

    'Chemicals': [
        r'\bpesticide\b', r'\bherbicide\b', r'\binsecticide\b', r'\bparaquat\b', r'\brotenone\b',
        r'\bglyphosate\b', r'\borganophosphate\b', r'\borganochlorine\b', r'\bDDT\b',
        r'\bendocrine\s+disrupt', r'\bEDC\b', r'\bBPA\b', r'\bbisphenol\b', r'\bphthalate\b',
        r'\bPFAS\b', r'\bPFOA\b', r'\bPFOS\b', r'\bper.?fluorin', r'\bforever\s+chemical',
        r'\bheavy\s+metal\b', r'\barsenic\b', r'\blead\s+(?:exposure|poison|toxic)',
        r'\bmercury\b', r'\bcadmium\b', r'\bchromium\b', r'\bnickel\s+(?:exposure|compound)',
        r'\bair\s+pollut', r'\bPM2\.?5\b', r'\bPM10\b', r'\bparticulate\s+matter\b',
        r'\bozone\s+(?:exposure|pollution)', r'\bNO2\b', r'\bnitrogen\s+dioxide\b',
        r'\bvolatile\s+organic\b', r'\bVOC\b', r'\bformaldehyde\b', r'\bbenzene\b',
        r'\basbestos\b', r'\bsilica\b', r'\bnanomaterial\b', r'\bnanoparticle\b',
        r'\btoxicant\b', r'\btoxin\b', r'\bxenobiotic\b', r'\bcarcinogen\b',
        r'\bcontaminant\b', r'\bexposure\b.*(?:chemical|toxic|pollut|industrial)',
        r'\boccupational\s+(?:exposure|hazard)', r'\benvironmental\s+(?:exposure|toxin|contam)',
        r'\bdioxin\b', r'\bPCB\b', r'\bpolychlorinated\b', r'\bAhR\b', r'\baryl\s+hydrocarbon',
        r'\bdetoxifi', r'\bglutathione\b', r'\bNrf2\b', r'\bCYP450\b', r'\bCYP1A', r'\bCYP2',
        r'\bmicrocystin\b', r'\baflatoxin\b', r'\bmycotoxin\b', r'\bracdon\b',
        r'\bacrolein\b', r'\btrichloroethylene\b', r'\bTCE\b', r'\bperchloroethylene\b',
    ],

    'Infections': [
        r'\bvirus\b', r'\bviral\b', r'\binfection\b', r'\binfectious\b', r'\bpathogen\b',
        r'\bbacteria\b(?!.*microbiome)', r'\bbacterial\b(?!.*microbiome|commensal|colonization)',
        r'\bfungal\b', r'\bparasit', r'\bHBV\b', r'\bHCV\b', r'\bhepatitis\b',
        r'\bHIV\b', r'\bHPV\b', r'\bEBV\b', r'\bCMV\b', r'\bHSV\b', r'\bherpes\b',
        r'\binfluenza\b', r'\bCOVID', r'\bSARS', r'\bcoronavirus\b', r'\bRSV\b',
        r'\bzoonotic\b', r'\bzoonoses\b', r'\bprion\b', r'\bsepsis\b', r'\bseptic\b',
        r'\btuberculosis\b', r'\bTB\b', r'\bmalaria\b', r'\bplasmodium\b',
        r'\blyme\b', r'\bborrelia\b', r'\bstaph', r'\bstreptococ', r'\be\.\s*coli\b',
        r'\bsalmonella\b', r'\bklebsiella\b', r'\bpneumonia\b', r'\bmeningitis\b',
        r'\bencephalitis\b', r'\bimmune\s+response\s+to\b', r'\bhost.?pathogen\b',
        r'\bantimicrobial\b', r'\bantibiotic\b', r'\bantiviral\b', r'\bantifungal\b',
        r'\bvaccine\b', r'\bimmunization\b', r'\bimmunogen', r'\bseroprevalence\b',
    ],

    'Diet_Nutrition': [
        r'\bdiet(?:ary)?\b', r'\bnutrition', r'\bfood\b', r'\bcalor', r'\bfasting\b',
        r'\bintermittent\s+fasting\b', r'\bketogenic\b', r'\bketo\s+diet\b',
        r'\bmediterranean\s+diet\b', r'\bwestern\s+diet\b', r'\bhigh.?fat\s+diet\b',
        r'\blow.?fat\s+diet\b', r'\bplant.?based\b', r'\bvegetarian\b', r'\bvegan\b',
        r'\bfiber\b', r'\bwhole\s+grain\b', r'\bfruit\b', r'\bvegetable\b',
        r'\bred\s+meat\b', r'\bprocessed\s+meat\b', r'\bsugar\b', r'\bfructose\b',
        r'\bglucose\b.*(?:diet|intake|consumption)', r'\bcarbohydrate\b',
        r'\bsaturated\s+fat\b', r'\btrans\s+fat\b', r'\bomega.?3\b', r'\bomega.?6\b',
        r'\bfatty\s+acid\b', r'\blipid\b.*(?:diet|intake)', r'\bcholesterol\b.*(?:diet|intake)',
        r'\bvitamin\b', r'\bfolate\b', r'\bfolic\s+acid\b', r'\bB12\b', r'\bvitamin\s+D\b',
        r'\bvitamin\s+C\b', r'\bvitamin\s+E\b', r'\bvitamin\s+A\b', r'\bretinoid\b',
        r'\biron\b.*(?:deficien|supplement|intake)', r'\bzinc\b.*(?:deficien|supplement)',
        r'\bcalcium\b.*(?:diet|intake|supplement)', r'\bmagnesium\b',
        r'\bselenium\b', r'\bpolyphenol\b', r'\bflavonoid\b', r'\bantioxidant\b.*(?:diet|food)',
        r'\bsupplement', r'\bnutraceutical\b', r'\bphytochemical\b',
        r'\bmalnutrition\b', r'\bundernutrition\b', r'\bovernutrition\b',
        r'\bfeeding\b.*(?:behavior|pattern|restrict)', r'\bfood\s+insecurity\b',
    ],

    'Obesity': [
        r'\bobes', r'\boverweight\b', r'\bBMI\b', r'\bbody\s+mass\s+index\b',
        r'\badiposity\b', r'\badipocyte\b', r'\badipokine\b', r'\badipose\b',
        r'\bleptin\b', r'\bghrelin\b', r'\bweight\s+(?:gain|loss|management|control)',
        r'\bbariatric\b', r'\bgastric\s+bypass\b', r'\bmetabolic\s+syndrome\b',
        r'\binsulin\s+resistance\b', r'\bhyperinsulin', r'\bglycemic\b',
        r'\bNAFLD\b', r'\bNASH\b', r'\bfatty\s+liver\b', r'\bhepatic\s+steatosis\b',
        r'\bvisceral\s+fat\b', r'\babdominal\s+fat\b', r'\bectopic\s+fat\b',
        r'\blipogenesis\b', r'\blipolysis\b', r'\benergy\s+(?:balance|expenditure|homeostasis)',
        r'\bthermogenesis\b', r'\bbrown\s+(?:fat|adipose)\b', r'\bWAT\b', r'\bBAT\b',
    ],
}

# Mechanistic terms that imply exposure influence even if not explicitly stated
MECHANISTIC_EXPOSURE_HINTS = {
    'Microbiome': [
        r'\bgut.?brain\s+axis\b', r'\bgut.?liver\s+axis\b', r'\benteric\s+nervous\b',
        r'\bintestinal\s+permeability\b', r'\bleaky\s+gut\b', r'\btight\s+junction\b.*(?:gut|intestin)',
        r'\bmucosal\s+immun', r'\bintestinal\s+epithelial\b', r'\bPeyer.?s\s+patch',
        r'\benterocyte\b', r'\bgoblet\s+cell\b', r'\bPaneth\s+cell\b',
        r'\bintestinal\s+inflammation\b', r'\bcolitis\b', r'\bIBD\b',
        r'\bLPS\b', r'\blipopolysaccharide\b', r'\bendotoxin\b',
    ],
    'Alcohol': [
        r'\bhepatic\s+stellate\b', r'\bKupffer\s+cell\b', r'\bfibrogenesis\b.*liver',
        r'\bliver\s+regeneration\b', r'\bhepatocyte\s+(?:injury|death|apoptosis)',
        r'\bsteatohepatitis\b', r'\bliver\s+inflammation\b',
    ],
    'Smoking': [
        r'\bairway\s+epithelial\b', r'\bbronchial\s+epithelial\b', r'\balveolar\b.*(?:damage|injury)',
        r'\bpulmonary\s+inflammation\b', r'\bCOPD\b', r'\bemphysema\b',
        r'\bsmall\s+airway\b', r'\bmucous\s+(?:hyperplasia|secretion)',
    ],
    'Chemicals': [
        r'\bDNA\s+damage\b', r'\bDNA\s+adduct\b', r'\bgenotoxic',
        r'\bproteotoxic\b', r'\bprotein\s+aggregat',
    ],
    'Infections': [
        r'\bTLR\d?\b', r'\btoll.?like\s+receptor\b', r'\binnate\s+immun',
        r'\binterferon\b', r'\bcytokine\s+storm\b',
        r'\bNF.?kB\b', r'\bimmune\s+evasion\b',
    ],
    'Obesity': [
        r'\bmetaflammation\b',
        r'\binsulin\s+signaling\b', r'\bglucose\s+(?:uptake|metabolism|homeostasis)',
        r'\bAMPK\b', r'\bmTOR\b.*(?:metabol|nutri|energy)',
    ],
}

# NEW: Mechanistic pathway categories that are influenced by environmental exposures
# These capture the "downstream effects" of exposures
MECHANISTIC_PATHWAY_PATTERNS = {
    'Inflammation_Pathway': [
        r'\binflammation\b', r'\binflammatory\b', r'\binflammasome\b', r'\bNLRP3\b',
        r'\bcytokine\b', r'\bchemokine\b', r'\binterleukin\b', r'\bIL-\d+\b', r'\bIL\d+\b',
        r'\bTNF\b', r'\btumor\s+necrosis\s+factor\b', r'\bNF.?kB\b', r'\bNF.?κB\b',
        r'\bCOX-?2\b', r'\bcyclooxygenase\b', r'\bprostaglandin\b',
        r'\bmacrophage\s+(?:activation|polarization|infiltration)', r'\bM1\s+macrophage\b',
        r'\bneutrophil\s+(?:infiltration|recruitment)', r'\binnate\s+immun',
        r'\bchronic\s+inflammation\b', r'\bsystemic\s+inflammation\b', r'\blow.?grade\s+inflammation\b',
        r'\bneuro.?inflammation\b', r'\bhepatic\s+inflammation\b', r'\blung\s+inflammation\b',
        r'\btissue\s+inflammation\b', r'\bmucosal\s+inflammation\b',
        r'\banti.?inflammatory\b', r'\bpro.?inflammatory\b',
        r'\bJAK.?STAT\b', r'\bSTAT3\b', r'\bIRAK\b', r'\bMyD88\b',
    ],

    'Mitochondrial_Dysfunction': [
        r'\bmitochondria\b', r'\bmitochondrial\b', r'\bmtDNA\b',
        r'\boxidative\s+phosphorylation\b', r'\bOXPHOS\b', r'\belectron\s+transport\s+chain\b',
        r'\bcomplex\s+[IV]+\b', r'\bATP\s+(?:synthase|production|depletion)',
        r'\bmitophagy\b', r'\bmitochondrial\s+(?:dysfunction|damage|stress|biogenesis|dynamics)',
        r'\bmitochondrial\s+(?:fission|fusion|fragmentation)', r'\bDrp1\b', r'\bMfn\d?\b',
        r'\bPGC.?1\b', r'\bTFAM\b', r'\bmitochondrial\s+membrane\s+potential\b',
        r'\bcytochrome\s+c\b', r'\bapoptosis\b.*mitochondria', r'\bmitochondria\b.*apoptosis',
        r'\bROS\b', r'\breactive\s+oxygen\s+species\b', r'\boxidative\s+stress\b',
        r'\bsuperoxide\b', r'\bhydrogen\s+peroxide\b', r'\bH2O2\b',
        r'\bantioxidant\b', r'\bSOD\b', r'\bcatalase\b', r'\bglutathione\b', r'\bGSH\b',
        r'\bNrf2\b', r'\bARE\b', r'\bredox\b', r'\bfree\s+radical\b',
        r'\blipid\s+peroxidation\b', r'\b4.?HNE\b', r'\bMDA\b', r'\bmalondialdehyde\b',
        r'\bnitrosative\s+stress\b', r'\bperoxynitrite\b', r'\bnitric\s+oxide\b.*(?:stress|damage)',
    ],

    'Epigenetic_Changes': [
        r'\bepigenetic\b', r'\bepigenome\b', r'\bepimutation\b',
        r'\bDNA\s+methylation\b', r'\bmethylation\b', r'\bhypermethylation\b', r'\bhypomethylation\b',
        r'\bDNMT\b', r'\bDNA\s+methyltransferase\b', r'\bCpG\b', r'\bCpG\s+island\b',
        r'\bhistone\b', r'\bchromatin\b', r'\bnucleosome\b',
        r'\bhistone\s+(?:modification|acetylation|methylation|deacetylation)',
        r'\bH3K\d+\b', r'\bH4K\d+\b', r'\bHDAC\b', r'\bHAT\b', r'\bKDM\b', r'\bKMT\b',
        r'\bchromatin\s+(?:remodeling|accessibility|modification)',
        r'\bATAC.?seq\b', r'\bChIP.?seq\b',
        r'\bimprinting\b', r'\bX.?inactivation\b',
        r'\btransgenerational\b', r'\bintergenerational\b', r'\bepigenetic\s+inheritance\b',
        r'\bm6A\b', r'\bRNA\s+methylation\b', r'\bepitranscriptom',
        r'\bmiRNA\b', r'\bmicroRNA\b', r'\blncRNA\b', r'\blong\s+non.?coding\s+RNA\b',
        r'\bnon.?coding\s+RNA\b', r'\bncRNA\b', r'\bsmall\s+RNA\b',
        r'\bgene\s+silencing\b', r'\btranscriptional\s+(?:silencing|repression)',
    ],

    # Broader mechanistic categories
    'Developmental_Origins': [
        r'\bmaternal\b', r'\bfetal\b', r'\bpregnancy\b', r'\bgestational\b',
        r'\bprenatal\b', r'\bperinatal\b', r'\bpostnatal\b', r'\bearly\s+life\b',
        r'\bin\s+utero\b', r'\bdevelopmental\s+(?:origin|programming)\b',
        r'\bDOHaD\b', r'\bplacenta\b', r'\bembryonic\b',
        r'\bbreastfeed\b', r'\blactation\b', r'\bneonatal\b',
        r'\bmaternal.?fetal\b', r'\bpregnant\b', r'\bgestation\b',
        r'\bpreterm\b', r'\bbirth\s+(?:weight|outcome)\b', r'\binfant\b',
    ],

    'Immune_Tumor_Interaction': [
        r'\bimmune\b', r'\bimmunity\b', r'\bimmunotherapy\b',
        r'\bT\s+cell\b', r'\bCD8\b', r'\bCD4\b', r'\bNK\s+cell\b',
        r'\bmacrophage\b', r'\bdendritic\s+cell\b',
        r'\bimmune\s+(?:evasion|escape|checkpoint|response|surveillance)\b',
        r'\bPD.?1\b', r'\bPD.?L1\b', r'\bCTLA.?4\b',
        r'\btumor\s+immun', r'\banti.?tumor\s+immun',
    ],

    'Social_Environmental_Determinants': [
        r'\bdisparities\b', r'\binequit', r'\bsocioeconomic\b', r'\bSES\b',
        r'\bneighborhood\b', r'\bracial\b', r'\bethnic\b',
        r'\bsocial\s+determinant\b', r'\bhealth\s+equity\b',
        r'\baccess\s+to\s+(?:care|health)\b', r'\bunderserved\b',
        r'\brural\b', r'\burban\b', r'\bgeographic\b',
        r'\bminority\b', r'\bAfrican\s+American\b', r'\bHispanic\b', r'\bLatino\b',
        r'\blow.?income\b', r'\bpoverty\b',
    ],

    'Signaling_Pathways': [
        r'\bsignaling\b', r'\bsignal\s+transduction\b',
        r'\bkinase\b', r'\bphosphorylation\b',
        r'\bWnt\b', r'\bNotch\b', r'\bHedgehog\b', r'\bMAPK\b', r'\bERK\b',
        r'\bPI3K\b', r'\bAKT\b', r'\bmTOR\b', r'\bRas\b',
        r'\bSmad\b', r'\bTGF.?β\b', r'\bTGFB\b', r'\bBMP\b',
        r'\bEGFR\b', r'\bHER2\b', r'\bVEGF\b', r'\bFGF\b',
    ],

    'Cardiovascular_Vascular': [
        r'\bcardiovascular\b', r'\bcardiac\b', r'\bheart\b',
        r'\bvascular\b', r'\bendothelial\b', r'\batherosclerosis\b',
        r'\bhypertens\b', r'\bblood\s+pressure\b', r'\bstroke\b',
        r'\bcoronary\b', r'\bmyocardial\b', r'\barterial\b',
        r'\bcardiomyopathy\b', r'\bheart\s+failure\b', r'\barrhythm',
    ],

    'Drug_Resistance': [
        r'\bresistance\b', r'\bresistant\b', r'\brefractory\b',
        r'\bdrug\s+resistance\b', r'\bchemoresistance\b', r'\btherapy\s+resistance\b',
        r'\bmultidrug\b', r'\bMDR\b', r'\befflux\b',
        r'\btreatment.?resist', r'\brecurren',
    ],

    'Physical_Activity_Lifestyle': [
        r'\bphysical\s+activity\b', r'\bexercise\b', r'\bsedentary\b',
        r'\blifestyle\b', r'\bweight\s+(?:loss|management|control)\b',
        r'\bfitness\b', r'\baerobic\b', r'\bstrength\s+training\b',
    ],

    'Metabolism_Energy': [
        r'\bmetabolis\b', r'\bmetabolic\b', r'\bbioenergetic\b',
        r'\bglycolysis\b', r'\bWarburg\b', r'\bglutamine\b',
        r'\blipid\s+metabolism\b', r'\bfatty\s+acid\b', r'\blipogenesis\b',
        r'\bglucose\s+metabolism\b', r'\bATP\b', r'\bNAD\b',
        r'\bmitochondrial\s+metabolism\b', r'\boxidative\s+metabolism\b',
        r'\bketone\b', r'\bketogenic\b', r'\blactate\b',
    ],

    'Gene_Regulation_Transcription': [
        r'\bgene\s+(?:expression|regulation)\b',
        r'\btranscription\b', r'\btranscriptional\b', r'\btranscriptome\b',
        r'\bpromoter\b', r'\benhancer\b', r'\bregulatory\s+element\b',
        r'\bRNA\s+(?:processing|splicing|stability)\b', r'\bsplicing\b',
        r'\bpost.?transcriptional\b',
    ],

    'Cellular_Stress_Response': [
        r'\bstress\s+response\b', r'\bcellular\s+stress\b',
        r'\bER\s+stress\b', r'\bUPR\b', r'\bunfolded\s+protein\b',
        r'\bheat\s+shock\b', r'\bHSP\b', r'\bchaperone\b',
        r'\bproteotoxic\b', r'\bcytotoxic\b', r'\bgenotoxic\b',
        r'\bDNA\s+damage\s+response\b', r'\bDDR\b',
    ],

    'Tumor_Microenvironment': [
        r'\btumor\s+microenvironment\b', r'\bTME\b', r'\bstroma\b', r'\bstromal\b',
        r'\btumor\s+(?:stroma|infiltrat)\b', r'\bcancer.?associated\s+fibroblast\b',
        r'\bCAF\b', r'\btumor.?infiltrating\b', r'\bTIL\b',
        r'\bangiogenesis\b', r'\bvasculature\b', r'\btumor\s+vasculat',
    ],

    'Autophagy_Proteostasis': [
        r'\bautophagy\b', r'\bautophagic\b', r'\bproteostasis\b',
        r'\bproteasome\b', r'\bubiquitin\b', r'\blysosome\b', r'\blysosomal\b',
        r'\bprotein\s+(?:degradation|clearance|aggregat|misfolding)\b',
    ],

    'Fibrosis': [
        r'\bfibrosis\b', r'\bfibrotic\b', r'\bfibrogenesis\b',
        r'\bcollagen\s+deposition\b', r'\bextracellular\s+matrix\b', r'\bECM\b',
        r'\bmyofibroblast\b', r'\bstellate\s+cell\b',
    ],

    'Senescence_Aging': [
        r'\bsenescen', r'\bcellular\s+aging\b',
        r'\btelomer\b', r'\breplicative\s+(?:aging|senescence)\b',
        r'\bp16\b', r'\bp21\b', r'\bSASP\b', r'\bsenolytic\b',
        r'\blongevity\b', r'\bhealthspan\b',
    ],

    'Endocrine_Hormonal': [
        r'\bhormone\b', r'\bhormonal\b', r'\bendocrine\b',
        r'\bestrogen\b', r'\bandrogen\b', r'\btestosterone\b', r'\bprogesterone\b',
        r'\bthyroid\b', r'\bcortisol\b', r'\bglucocorticoid\b',
        r'\bHPA\s+axis\b', r'\bHPG\s+axis\b', r'\bmenopausal\b', r'\bmenopause\b',
    ],

    'Neurodegeneration': [
        r'\balpha.?synuclein\b', r'\bα.?synuclein\b', r'\bsynuclein\b',
        r'\btau\s+(?:protein|phosphorylation|aggregat|pathology)\b',
        r'\bamyloid\b', r'\bAβ\b', r'\bplaque\b',
        r'\bLewy\s+bod', r'\bneurofibrill', r'\bTDP.?43\b',
        r'\bprotein\s+aggregat\b', r'\bneurodegenerat',
        r'\bdopamin\b', r'\bmotor\s+neuron\b',
    ],

    # Additional categories for uncategorized grants
    'Biomarker_Detection': [
        r'\bbiomarker\b', r'\bscreening\b', r'\bearly\s+detect', r'\bdiagnos',
        r'\bprognos', r'\brisk\s+(?:predict|assess|stratif)',
        r'\bliquid\s+biopsy\b', r'\bctDNA\b', r'\bcirculating\s+tumor',
        r'\bmarker\b', r'\bpredictive\s+(?:marker|value|factor)',
        r'\bdiagnostic\b', r'\bprognostic\b',
    ],

    'Behavioral_Psychosocial': [
        r'\bbehavior\b', r'\bbehavioral\b', r'\bintervention\b',
        r'\badherence\b', r'\bcounseling\b', r'\bpsycholog',
        r'\bmental\s+health\b', r'\bcognitive\b', r'\bdepression\b', r'\banxiety\b',
        r'\bstress\b(?!.*oxidative|.*cellular|.*ER)', r'\btrauma\b',
        r'\bquality\s+of\s+life\b', r'\bwell.?being\b', r'\bpsychosocial\b',
        r'\bPTSD\b', r'\bsubstance\s+(?:use|abuse)\b', r'\baddiction\b',
    ],

    'Imaging_Technology': [
        r'\bimaging\b', r'\bMRI\b', r'\bPET\b', r'\bCT\s+scan\b',
        r'\bultrasound\b', r'\bmammograph\b', r'\bradiograph\b', r'\btomograph\b',
        r'\bmicroscop\b', r'\bfluorescen\b', r'\bspectroscop\b',
        r'\boptical\b', r'\bvisualization\b', r'\bcontrast\s+agent\b',
    ],

    'Cell_Death_Apoptosis': [
        r'\bapoptos', r'\bcell\s+death\b', r'\bnecrosis\b', r'\bnecroptosis\b',
        r'\bprogrammed\s+death\b', r'\bferroptosis\b', r'\bpyroptosis\b',
        r'\banoikis\b', r'\bcaspase\b', r'\bBcl.?2\b', r'\bBax\b',
    ],

    'Stem_Cell_Regeneration': [
        r'\bstem\s+cell\b', r'\bprogenitor\b', r'\bpluripoten\b',
        r'\biPSC\b', r'\borganoid\b', r'\bself.?renew\b',
        r'\bregenerat', r'\bdifferentiat',
    ],

    'DNA_Repair_Damage': [
        r'\bDNA\s+repair\b', r'\bDNA\s+damage\b', r'\bmutagene\b',
        r'\bBRCA\b', r'\bhomologous\s+recomb', r'\bmismatch\s+repair\b',
        r'\bnucleotide\s+excision\b', r'\bbase\s+excision\b',
        r'\bdouble.?strand\s+break\b', r'\bDSB\b', r'\bHR\b', r'\bNHEJ\b',
        r'\bgenome\s+(?:stability|instability|integrity)\b',
    ],
}


def classify_grant_by_exposure(title, original_tag, original_subgroup):
    """
    Classify a grant by exposure type based on its title.
    Returns a tuple of (direct_exposures, mechanistic_pathways).
    """
    title_lower = title.lower() if pd.notna(title) else ""
    exposures = []
    pathways = []

    # Check explicit exposure patterns
    for exposure, patterns in EXPOSURE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, title_lower, re.IGNORECASE):
                exposures.append(exposure)
                break

    # For mechanistic grants, check for implied exposure relationships
    if original_tag and 'mechanistic' in str(original_tag).lower():
        for exposure, patterns in MECHANISTIC_EXPOSURE_HINTS.items():
            if exposure not in exposures:  # Don't double-count
                for pattern in patterns:
                    if re.search(pattern, title_lower, re.IGNORECASE):
                        exposures.append(exposure)
                        break

    # Check for mechanistic pathway patterns (inflammation, mitochondria, epigenetics)
    for pathway, patterns in MECHANISTIC_PATHWAY_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, title_lower, re.IGNORECASE):
                pathways.append(pathway)
                break

    # Use original environmental subgroup if available and not already captured
    if pd.notna(original_subgroup) and original_subgroup:
        subgroup = str(original_subgroup).strip()
        subgroup_mapping = {
            'Smoking': 'Smoking',
            'Chemicals': 'Chemicals',
            'Microbiome': 'Microbiome',
            'Diet/Nutrition': 'Diet_Nutrition',
            'Diet_Nutrition': 'Diet_Nutrition',
            'Alcohol': 'Alcohol',
            'Infection': 'Infections',
            'Radiation': 'Radiation',
            'Gene-Env': 'Gene_Environment',
            'Other': None,  # Don't add "Other" as an exposure
        }
        mapped = subgroup_mapping.get(subgroup)
        if mapped and mapped not in exposures:
            exposures.append(mapped)

    return list(set(exposures)), list(set(pathways))


def main():
    base_path = Path('/Users/sarahdaniels/Documents/grant_categorization/disease_area_grants')
    output_path = Path('/Users/sarahdaniels/Documents/grant_categorization/disease_by_exposures')

    # Files to process
    csv_files = [
        'als_reclassified_corrected.csv',
        'breast_cancer_classified.csv',
        'colorectal_cancer_reclassified_corrected.csv',
        'lung_cancer_reclassified_final_v3.csv',
        'parkinsons_corrected_final.csv',
        'Biodefense_classified.csv',
        'Contraception_Reproduction_classified.csv',
        'Liver_Disease_classified.csv',
        'womens_health_corrected_v3.csv',
    ]

    all_grants = []

    for csv_file in csv_files:
        filepath = base_path / csv_file
        if filepath.exists():
            print(f"Processing {csv_file}...")

            # Some files have an extra header row - check and skip if needed
            with open(filepath, 'r') as f:
                first_line = f.readline()

            skip_rows = 1 if 'Project Listing' in first_line else 0
            df = pd.read_csv(filepath, skiprows=skip_rows)

            # Normalize column names
            df.columns = df.columns.str.strip()

            # Find the right columns
            title_col = None
            tag_col = None
            subgroup_col = None

            for col in df.columns:
                if 'title' in col.lower():
                    title_col = col
                if 'tag' in col.lower():
                    tag_col = col
                if 'subgroup' in col.lower() or 'environmental_sub' in col.lower():
                    subgroup_col = col

            if title_col is None:
                print(f"  Warning: No title column found in {csv_file}")
                continue

            # Process each grant
            for idx, row in df.iterrows():
                title = row.get(title_col, '')
                original_tag = row.get(tag_col, '') if tag_col else ''
                original_subgroup = row.get(subgroup_col, '') if subgroup_col else ''

                exposures, pathways = classify_grant_by_exposure(title, original_tag, original_subgroup)

                # Combine exposures and pathways for total categorization
                all_categories = exposures + pathways

                grant_data = {
                    'Disease_Area': row.get('Category', csv_file.replace('_classified.csv', '').replace('_reclassified_corrected.csv', '').replace('_corrected_final.csv', '')),
                    'Appl_id': row.get('Appl_id', ''),
                    'FY': row.get('FY', ''),
                    'Funding_IC': row.get('Funding IC', row.get('Funding_IC', '')),
                    'Project_Number': row.get('Project Number', row.get('Project_Number', '')),
                    'Project_Title': title,
                    'PI_Name': row.get('PI_Name', row.get('PI Name', '')),
                    'Org_Name': row.get('Org Name', row.get('Org_Name', '')),
                    'State_Country': row.get('State / Country', row.get('State_Country', '')),
                    'Amount': row.get('Amount', ''),
                    'Original_Tag': original_tag,
                    'Original_Subgroup': original_subgroup,
                    'Exposure_Categories': '|'.join(exposures) if exposures else '',
                    'Mechanistic_Pathways': '|'.join(pathways) if pathways else '',
                    'All_Categories': '|'.join(all_categories) if all_categories else '',
                    'Num_Exposures': len(exposures),
                    'Num_Pathways': len(pathways),
                    'Num_Total': len(all_categories),
                }

                all_grants.append(grant_data)

    # Create DataFrame
    result_df = pd.DataFrame(all_grants)

    # Save all grants with exposure tags
    result_df.to_csv(output_path / 'all_grants_by_exposure.csv', index=False)

    # Create separate files for each exposure category
    exposure_counts = {}
    for exposure in list(EXPOSURE_PATTERNS.keys()) + ['Radiation', 'Gene_Environment']:
        exposure_df = result_df[result_df['Exposure_Categories'].str.contains(exposure, na=False)]
        if len(exposure_df) > 0:
            exposure_df.to_csv(output_path / f'{exposure.lower()}_grants.csv', index=False)
            exposure_counts[exposure] = len(exposure_df)

    # Create separate files for mechanistic pathway categories
    pathway_counts = {}
    for pathway in MECHANISTIC_PATHWAY_PATTERNS.keys():
        pathway_df = result_df[result_df['Mechanistic_Pathways'].str.contains(pathway, na=False)]
        if len(pathway_df) > 0:
            pathway_df.to_csv(output_path / f'{pathway.lower()}_grants.csv', index=False)
            pathway_counts[pathway] = len(pathway_df)

    # Statistics
    total_grants = len(result_df)
    has_exposure = len(result_df[result_df['Num_Exposures'] > 0])
    has_pathway = len(result_df[result_df['Num_Pathways'] > 0])
    has_any = len(result_df[result_df['Num_Total'] > 0])
    uncategorized = total_grants - has_any

    print("\n" + "="*70)
    print("CLASSIFICATION RESULTS")
    print("="*70)
    print(f"\nTotal grants processed: {total_grants:,}")
    print(f"\n--- DIRECT EXPOSURES ---")
    print(f"Grants with direct exposure category: {has_exposure:,} ({100*has_exposure/total_grants:.1f}%)")
    print(f"\n--- MECHANISTIC PATHWAYS (exposure-influenced) ---")
    print(f"Grants with mechanistic pathway: {has_pathway:,} ({100*has_pathway/total_grants:.1f}%)")
    print(f"\n--- COMBINED ---")
    print(f"Total categorized (exposure OR pathway): {has_any:,} ({100*has_any/total_grants:.1f}%)")
    print(f"Remaining uncategorized: {uncategorized:,} ({100*uncategorized/total_grants:.1f}%)")

    print("\n" + "-"*50)
    print("Direct Exposure Categories:")
    print("-"*50)
    for exposure, count in sorted(exposure_counts.items(), key=lambda x: -x[1]):
        print(f"  {exposure}: {count:,}")

    print("\n" + "-"*50)
    print("Mechanistic Pathway Categories (exposure-influenced):")
    print("-"*50)
    for pathway, count in sorted(pathway_counts.items(), key=lambda x: -x[1]):
        print(f"  {pathway}: {count:,}")

    # Overlap stats
    has_both = len(result_df[(result_df['Num_Exposures'] > 0) & (result_df['Num_Pathways'] > 0)])
    pathway_only = len(result_df[(result_df['Num_Exposures'] == 0) & (result_df['Num_Pathways'] > 0)])
    print(f"\n--- OVERLAP ---")
    print(f"Grants with BOTH exposure AND pathway: {has_both:,}")
    print(f"Grants with pathway ONLY (no direct exposure): {pathway_only:,}")

    # By disease area
    print("\n" + "-"*50)
    print("By Disease Area:")
    print("-"*50)
    for disease in result_df['Disease_Area'].unique():
        if pd.isna(disease) or disease == 'nan':
            continue
        disease_df = result_df[result_df['Disease_Area'] == disease]
        disease_exp = len(disease_df[disease_df['Num_Exposures'] > 0])
        disease_path = len(disease_df[disease_df['Num_Pathways'] > 0])
        disease_any = len(disease_df[disease_df['Num_Total'] > 0])
        print(f"  {disease}:")
        print(f"    Direct exposures: {disease_exp:,}/{len(disease_df):,}")
        print(f"    Mech pathways: {disease_path:,}/{len(disease_df):,}")
        print(f"    Total categorized: {disease_any:,}/{len(disease_df):,} ({100*disease_any/len(disease_df):.1f}%)")

    print("\n" + "="*70)
    print(f"Output files saved to: {output_path}")
    print("="*70)


if __name__ == '__main__':
    main()
