
##____________________________________________________________________________||
import FWCore.ParameterSet.Config as cms

##____________________________________________________________________________||
process = cms.Process("FILT")

##____________________________________________________________________________||
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')
options.register('certFile', '', VarParsing.multiplicity.singleton, VarParsing.varType.string, "json file")
options.inputFiles = 'file:/afs/cern.ch/cms/Tutorials/TWIKI_DATA/MET/MET_Run2012C_AOD_532_numEvent100.root',
options.outputFile = 'filters_tag.root'
options.maxEvents = -1
options.parseArguments()

print options.inputFiles

##____________________________________________________________________________||
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load("Configuration.Geometry.GeometryIdeal_cff")

process.options   = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(options.maxEvents))

##____________________________________________________________________________||
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string("FT_R_53_V21::All")

##____________________________________________________________________________||
process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles)
    )

##____________________________________________________________________________||
if options.certFile:
    import FWCore.PythonUtilities.LumiList as LumiList
    process.source.lumisToProcess = LumiList.LumiList(filename = options.certFile).getVLuminosityBlockRange()

##____________________________________________________________________________||
process.load("RecoMET.METFilters.metFilters_cff")

process.Flag_HBHENoiseFilter  = cms.Path(process.HBHENoiseFilter)
process.Flag_CSCTightHaloFilter = cms.Path(process.CSCTightHaloFilter)
process.Flag_hcalLaserEventFilter = cms.Path(process.hcalLaserEventFilter)
process.Flag_EcalDeadCellTriggerPrimitiveFilter = cms.Path(process.EcalDeadCellTriggerPrimitiveFilter)
process.Flag_goodVertices = cms.Path(process.goodVertices)
process.Flag_trackingFailureFilter = cms.Path(process.trackingFailureFilter)
process.Flag_eeBadScFilter = cms.Path(process.eeBadScFilter)
process.Flag_ecalLaserCorrFilter = cms.Path(process.ecalLaserCorrFilter)
process.Flag_trkPOGFilters = cms.Path(process.trkPOGFilters)

##____________________________________________________________________________||
process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string(options.outputFile),
    outputCommands = cms.untracked.vstring(
        'drop *',
        'keep *_*_*_FILT',
        ),
    SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('*', '!*'))
    )

process.outpath = cms.EndPath(process.out)

##____________________________________________________________________________||
