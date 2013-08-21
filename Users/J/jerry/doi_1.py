import scraperwiki

import lxml.etree as et

'''
list_DOIs = ['10.1002/hep.24509', '10.1007/JHEP11(2010)119', '10.1104/pp.112.200303', '10.1007/978-3-642-34234-9_21', '10.1007/978-3-642-34234-9_34', '10.1016/j.tcb.2009.11.004', '10.1073/pnas.1010833108', '10.1103/PhysRevA.84.013603', '10.1103/PhysRevA.85.043401', '10.1103/PhysRevLett.105.153604', '10.1128/MCB.01500-09', '10.1140/epjd/e2011-20071-x', '10.1182/blood-2010-10-313643', '10.1209/0295-5075/98/30005', '10.2337/dc09-0324', '10.1002/anie.201108849', '10.1002/cbic.201100282', '10.1007/JHEP01(2011)030', '10.1007/JHEP01(2012)006', '10.1007/JHEP05(2011)003', '10.1007/JHEP10(2010)042', '10.1021/am200811c', '10.1073/pnas.1120774109', '10.1088/1126-6708/2009/08/092', '10.1088/1126-6708/2009/10/030', '10.1088/1126-6708/2009/10/032', '10.1111/j.1742-4658.2010.07867.x', '10.1201/b11279-22', '10.1016/j.bmcl.2011.08.057', '10.1016/j.cell.2009.01.049', '10.1016/j.drudis.2011.06.003', '10.1016/j.jbiomech.2012.05.019', '10.1016/j.jtbi.2010.10.025', '10.1029/2009JC006087', '10.1038/nature10196', '10.1038/onc.2011.519', '10.1088/0004-637X/721/1/777', '10.1088/0004-637X/724/2/1396', '10.1088/0004-637X/727/1/15', '10.1088/0004-637X/736/2/159', '10.1088/0004-637X/741/2/76', '10.1088/0004-637X/741/2/97', '10.1088/2041-8205/747/1/L5', '10.1103/PhysRevLett.105.257001', '10.1111/j.1365-2958.2010.07493.x', '10.1111/j.1365-2958.2011.07840.x', '10.1111/j.1558-5646.2010.01176.x', '10.1111/j.1558-5646.2010.01185.x', '10.1111/j.1558-5646.2011.01477.x', '10.1186/1471-2407-12-209', '10.1371/journal.pone.0012230', '10.1091/mbc.E10-05-0408', '10.1109/EDCC.2012.11', '10.1109/PRDC.2011.36', '10.1002/bio.2341', '10.1002/bio.2341', '10.1002/cphc.201100504', '10.1002/ejoc.201000491', '10.1002/jcc.23040', '10.1002/wcms.97', '10.1007/s00214-010-0854-z', '10.1007/s00367-011-0271-x', '10.1016/j.bbadis.2008.10.020,', '10.1016/j.bbrc.2009.10.047', '10.1016/j.biochi.2011.01.016', '10.1016/j.bmcl.2011.11.010', '10.1016/j.bmc.2010.12.009', '10.1016/j.ejmg.2009.06.006', '10.1016/j.envsoft.2011.07.003', '10.1016/j.jmarsys.2011.04.001', '10.1016/j.jmarsys.2011.07.007', '10.1016/j.ocemod.2009.12.004', '10.1016/j.ocemod.2011.09.004', '10.1016/j.pocean.2010.05.002', '10.1016/j.rse.2009.09.003', '10.1016/j.rse.2010.04.002', '10.1016/j.rse.2011.04.013', '10.1016/j.rse.2011.05.019', '10.1016/j.rse.2011.09.020', '10.1016/j.rse.2011.11.019', '10.1016/j.scitotenv.2010.07.021', '10.1016/j.semcdb.2010.01.009,', '10.1016/j.tetlet.2010.10.113', '10.1016/j.ymgme.2007.08.118', '10.1021/ct2004758', '10.1021/ct200646r', '10.1021/ct300153f', '10.1021/ct300356j', '10.1021/ct3006562', '10.1021/ct300722e', '10.1021/jp300583h', '10.1029/2009JC006087', '10.1029/2010GL045934', '10.1029/2010JC006637', '10.1039/C1JM12457A', '10.1039/9781849734882-00042', '10.1063/1.4730301', '10.1086/657622', '10.1088/0957-4484/22/7/075703', '10.1109/LGRS.2009.2031825', '10.1109/LGRS.2011.2170659', '10.1109/LGRS.2012.2189753', '10.1109/TGRS.2010.2052813', '10.1111/php.12007', '10.1137/09076756X', '10.1175/MWR-D-10-05025.1', '10.1175/2011MWR3150.1', '10.1364/OE.19.025657', '10.5194/osd-9-1085-2012', '10.5194/osd-9-1349-2012', '10.5194/osd-9-1437-2012', '10.5194/osd-9-1481-2012', '10.5194/osd-9-1577-2012', '10.5194/osd-9-1599-2012', '10.5194/osd-9-1887-2012', '10.5194/osd-9-2081-2012', '10.5194/osd-9-291-2012', '10.5194/osd-9-499-2012', '10.5194/osd-9-687-2012', '10.5194/os-5-495-2009', '10.5194/os-6-247-2010', '10.5194/os-6-25-2010', '10.5194/os-6-61-2010', '10.5194/os-7-175-2011', '10.5194/os-7-771-2011', '10.5194/os-8-143-2012', '10.1098/rspb.2012.0147', '10.1242/jcs.069963', '10.1126/science.1221140', '10.1121/1.4708385', '10.1002/anie.201007409', '10.1002/adfm.201102227', '10.1002/adma.201101065', '10.1002/adma.201102378', '10.1002/adma.201102730', '10.1002/adma.201104497', '10.1002/adma.201202612', '10.1002/adsc.201100278', '10.1002/anie.200901308', '10.1002/anie.200902152', '10.1002/anie.201100193', '10.1002/anie.201107532', '10.1002/anie.201108450', '10.1002/anie.201109061', '10.1002/anie.201203929', '10.1002/art.27729', '10.1002/biot.201000346', '10.1002/biot.201000390', '10.1002/cbic.200900641', '10.1002/cbic.201000542', '10.1002/cbic.201000574', '10.1002/cbic.201100223', '10.1002/cctc.201000306', '10.1002/ceat.201100465', '10.1002/chem.201103418', '10.1002/chem.201103479', '10.1002/cne.21908', '10.1002/cphc.201100808', '10.1002/cphc.201100900', '10.1002/cphc.201200087', '10.1002/dvdy.22727', '10.1002/eet.586', '10.1002/ejoc.200900620', '10.1002/emmm.201200241', '10.1002/eqe.970', '10.1002/glia.20796', '10.1002/glia.20993', '10.1002/glia.21120', '10.1002/glia.21169', '10.1002/glia.21259', '10.1002/glia.22313', '10.1002/glia.22318', '10.1002/glia.22328', '10.1002/hep.22294', '10.1002/hep.23469', '10.1002/humu.21085', '10.1002/jctb.2681', '10.1002/jnr.22437', '10.1002/nme.3192', '10.1002/path.2344', '10.1002/prop.201200027', '10.1002/pssb.200879568', '10.1002/pssb.201000098', '10.1002/smll.201001044', '10.1002/9780470682531.pat0573', '10.1002/9783527633418.ch21', '10.1006/excr.2001.5263', '10.1007/JHEP01(2010)122', '10.1007/JHEP01(2011)146', '10.1007/JHEP02(2012)064', '10.1007/JHEP03(2011)120', '10.1007/JHEP03(2012)002', '10.1007/JHEP04(2012)096', '10.1007/JHEP05(2011)101', '10.1007/JHEP05(2012)102', '10.1007/JHEP05(2012)105', '10.1007/JHEP05(2012)138', '10.1007/JHEP06(2012)175', '10.1007/JHEP07(2011)112', '10.1007/JHEP08(2011)154', '10.1007/JHEP08(2012)164', '10.1007/JHEP09(2011)073', '10.1007/JHEP09(2011)095', '10.1007/JHEP10(2010)063', '10.1007/JHEP11(2010)005', '10.1007/JHEP11(2010)123', '10.1007/JHEP11(2010)151', '10.1007/JHEP11(2011)118', '10.1007/JHEP12(2010)074', '10.1007/JHEP12(2010)088', '10.1007/JHEP12(2011)036', '10.1007/JHEP12(2011)052', '10.1007/JHEP12(2011)088', '10.1007/s00039-010-0063-x', '10.1007/s00125-011-2238-x', '10.1007/s00213-011-2426-x', '10.1007/s00221-009-1881-7', '10.1007/s00285-011-0425-5', '10.1007/s00401-008-0354-6', '10.1007/s10346-010-0200-5', '10.1007/s10346-011-0299-z', '10.1007/s10534-011-9420-y', '10.1007/s10545-009-1297-3', '10.1007/s10584-011-0325-0', '10.1007/s10847-011-0016-5', '10.1007/s10847-011-9954-1', '10.1007/s10915-010-9380-3', '10.1007/s10948-009-0468-7', '10.1007/s11042-011-0943-6', '10.1007/s11051-012-1045-8', '10.1007/s11069-009-9431-y', '10.1007/s11069-010-9634-2', '10.1007/s11123-011-0223-5', '10.1007/s11157-010-9201-z', '10.1007/s11187-009-9187-5', '10.1007/s11207-010-9612-6', '10.1007/s11214-009-9561-2', '10.1007/s11242-009-9386-1', '10.1007/s11356-012-0939-4', '10.1007/s11661-011-0786-9', '10.1007/s12544-010-0035-0', '10.1007/s12544-010-0042-1', '10.1007/s12544-011-0050-9', '10.1007/s12544-011-0052-7', '10.1007/s13295-011-0014-5', '10.1007/s13311-011-0039-z', '10.1007/978-3-540-77655-0_9', '10.1007/978-3-642-15114-9_48', '10.1007/978-3-642-15155-2_42', '10.1007/978-3-642-15745-5_47', '10.1007/978-3-642-15835-3_26', '10.1007/978-3-642-15961-9', '10.1007/978-3-642-20712-9_28', '10.1007/978-3-642-21028-0_50', '10.1007/978-3-642-21347-2_3', '10.1007/978-3-642-21387-8_23', '10.1007/978-3-642-21732-6_1', '10.1007/978-3-642-22012-8_15', '10.1007/978-3-642-25167-2', '10.1007/978-3-642-30476-7_17', '10.1007/978-3-642-30642-6_21', '10.1007/978-3-642-31401-8_14', '10.1007/978-3-642-31623-4_2', '10.1007/978-3-642-31653-1_19', '10.1007/978-3-642-32589-2_49', '10.1007/978-3-642-33119-0_13', '10.1007/978-3-642-33212-8_15', '10.1007/978-3-642-34234-9_36', '10.1007/978-90-481-9641-8_5', '10.1016/B978-0-12-396533-2.00003-3', '10.1016/j.actamat.2011.01.027', '10.1016/j.actamat.2011.02.035', '10.1016/j.actamat.2012.01.002', '10.1016/j.actamat.2012.01.010', '10.1016/j.ajhg.2008.03.021', '10.1016/j.ajhg.2011.12.018', '10.1016/j.apcatb.2010.06.017', '10.1016/j.apcatb.2010.08.011', '10.1016/j.apcatb.2011.06.039', '10.1016/j.apcatb.2011.11.041', '10.1016/j.apcatb.2012.01.029', '10.1016/j.apcatb.2012.03.010', '10.1016/j.apcatb.2012.04.042', '10.1016/j.apcatb.2012.04.045', '10.1016/j.apcatb.2012.05.028', '10.1016/j.apcatb.2012.05.036', '10.1016/j.autrev.2009.12.013', '10.1016/j.autrev.2012.07.011', '10.1016/j.bbamem.2011.10.016', '10.1016/j.bbi.2011.03.018', '10.1016/j.bbrc.2010.10.030', '10.1016/j.biochi.2009.05.003', '10.1016/j.biochi.2012.05.007', '10.1016/j.biochi.2012.05.029', '10.1016/j.biocon.2011.04.018', '10.1016/j.bmc.2010.05.048', '10.1016/j.bmc.2010.05.048', '10.1016/j.bone.2011.03.414', '10.1016/j.bone.2011.03.425', '10.1016/j.brainresrev.2009.10.004', '10.1016/j.brainresrev.2009.10.005', '10.1016/j.brainresrev.2009.11.005', '10.1016/j.brainresrev.2009.11.007', '10.1016/j.brainresrev.2009.12.003', '10.1016/j.brainresrev.2010.02.003', '10.1016/j.brainres.2009.12.011', '10.1016/j.brainres.2012.06.045', '10.1016/j.carbon.2009.12.047', '10.1016/j.cattod.2010.02.016', '10.1016/j.cattod.2010.11.081', '10.1016/j.cattod.2011.02.014', '10.1016/j.cattod.2011.12.008', '10.1016/j.cbpa.2009.02.037', '10.1016/j.cej.2010.07.044', '10.1016/j.cej.2010.09.063', '10.1016/j.cej.2010.11.027', '10.1016/j.cej.2010.11.047', '10.1016/j.cej.2011.06.022', '10.1016/j.cej.2011.08.063', '10.1016/j.cej.2011.10.072', '10.1016/j.cej.2012.03.054', '10.1016/j.cell.2011.08.006', '10.1016/j.ces.2011.10.060', '10.1016/j.clay.2012.03.003', '10.1016/j.corsci.2010.07.027', '10.1016/j.corsci.2011.05.057', '10.1016/j.crte.2011.09.007', '10.1016/j.cub.2009.11.018', '10.1016/j.ejpain.2010.08.004', '10.1016/j.electacta.2012.07.037', '10.1016/j.elspec.2012.05.009', '10.1016/j.elspec.2012.06.005', '10.1016/j.enggeo.2010.01.003', '10.1016/j.enggeo.2010.04.017', '10.1016/j.eplepsyres.2008.12.006', '10.1016/j.eplepsyres.2010.03.014', '10.1016/j.eplepsyres.2010.06.011', '10.1016/j.eplepsyres.2010.06.015', '10.1016/j.eplepsyres.2011.07.011', '10.1016/j.expneurol.2011.08.012', '10.1016/j.expneurol.2011.08.024', '10.1016/j.expneurol.2011.09.033', '10.1016/j.febslet.2010.05.029', '10.1016/j.geomorph.2010.02.007', '10.1016/j.geomorph.2010.09.001', '10.1016/j.geomorph.2010.10.038', '10.1016/j.geomorph.2011.12.006', '10.1016/j.heares.2009.05.007', '10.1016/j.ica.2010.06.040', '10.1016/j.ijms.2012.02.026', '10.1016/j.it.2011.09.007', '10.1016/j.jbiotec.2011.10.002', '10.1016/j.jcat.2012.05.002', '10.1016/j.jcis.2010.03.067', '10.1016/j.jcis.2010.05.061', '10.1016/j.jcis.2012.04.053', '10.1016/j.jconhyd.2011.02.001', '10.1016/j.jcss.2009.10.007', '10.1016/j.jcss.2010.08.010', '10.1016/j.jhazmat.2011.09.081', '10.1016/j.jhazmat.2011.11.042', '10.1016/j.jhazmat.2012.01.032', '10.1016/j.jhazmat.2012.02.017', '10.1016/j.jip.2010.09.020', '10.1016/j.jmbbm.2011.03.018', '10.1016/j.jmb.2008.08.011', '10.1016/j.jmb.2008.12.006', '10.1016/j.jprot.2011.12.039', '10.1016/j.jsb.2009.07.001', '10.1016/j.jtbi.2011.06.018', '10.1016/j.media.2011.06.010', '10.1016/j.mee.2010.12.001', '10.1016/j.memsci.2011.01.014', '10.1016/j.memsci.2011.04.046', '10.1016/j.memsci.2011.12.028', '10.1016/j.memsci.2011.12.031', '10.1016/j.molcel.2012.03.017', '10.1016/j.msea.2010.12.018', '10.1016/j.nbd.2009.06.016', '10.1016/j.nbd.2011.03.013', '10.1016/j.nbd.2011.05.015', '10.1016/j.neulet.2011.10.032', '10.1016/j.neumeth.2010.12.021', '10.1016/j.neuroimage.2011.12.002', '10.1016/j.neuron.2008.01.029', '10.1016/j.neuron.2010.08.043', '10.1016/j.neuropharm.2009.09.012', '10.1016/j.neuropsychologia.2011.03.037', '10.1016/j.neuroscience.2010.02.047', '10.1016/j.neuroscience.2010.07.004', '10.1016/j.neuroscience.2011.01.020', '10.1016/j.neuroscience.2011.05.003', '10.1016/j.nlm.2010.09.002', '10.1016/j.nuclphysb.2009.05.005', '10.1016/j.nuclphysb.2010.08.011', '10.1016/j.nuclphysb.2012.01.003', '10.1016/j.pbiomolbio.2011.07.007', '10.1016/j.pbi.2012.03.008', '10.1016/j.proeng.2010.09.042', '10.1016/j.proenv.2011.02.022', '10.1016/j.pss.2009.04.004', '10.1016/j.pss.2009.07.011', '10.1016/j.pss.2009.07.014', '10.1016/j.respol.2007.09.003', '10.1016/j.respol.2010.02.012', '10.1016/j.respol.2011.05.013', '10.1016/j.respo1.2010.05.014', '10.1016/j.rse.2011.11.002', '10.1016/j.seppur.2011.06.001', '10.1016/j.seppur.2012.02.018', '10.1016/j.seppur.2012.03.031', '10.1016/j.snb.2009.11.066', '10.1016/j.snb.2010.10.050', '10.1016/j.snb.2012.03.057', '10.1016/j.stem.2010.11.017', '10.1016/j.susc.2009.11.030', '10.1016/j.synthmet.2010.09.006', '10.1016/j.tcb.2009.05.007', '10.1016/j.tins.2009.05.001', '10.1016/j.watres.2011.04.036', '10.1016/j.watres.2012.01.005', '10.1016/j.worlddev.2008.06.002', '10.1016/j.ydbio.2010.11.026', '10.1016/j.yexcr.2008.01.035', '10.1016/j.yexcr.2009.07.019', '10.1016/j.ympev.2010.08.012', '10.1017/S1462399406010751', '10.1017/S1740925X09000064', '10.1021/ac300372p', '10.1021/cg201358c', '10.1021/cr1002672', '10.1021/cs2003559', '10.1021/cs200575r', '10.1021/cs300142u', '10.1021/es100178f', '10.1021/es101293v', '10.1021/es2036527', '10.1021/es204176q', '10.1021/es801703k', '10.1021/es802019g', '10.1021/es803505u', '10.1021/ic102041q', '10.1021/ic201608j', '10.1021/ja106552p', '10.1021/ja109975c', '10.1021/ja201597b', '10.1021/ja205254s', '10.1021/ja2092272', '10.1021/ja210209r', '10.1021/ja211749b', '10.1021/ja303091q', '10.1021/ja9089846', '10.1021/jm101373a', '10.1021/jm201056j', '10.1021/jo101723v', '10.1021/jo102410r', '10.1021/jp100635e', '10.1021/jp1121068', '10.1021/jp200464d', '10.1021/jp2080918', '10.1021/jp2088803', '10.1021/jp302471p', '10.1021/jp303537v', '10.1021/jp9050353', '10.1021/jp905609x', '10.1021/jp910342b', '10.1021/jz101179f', '10.1021/la101414x', '10.1021/la102351f', '10.1021/la103097y', '10.1021/la103957v', '10.1021/la2005387', '10.1021/la2010387', '10.1021/la201595e', '10.1021/la2019132', '10.1021/la300365q', '10.1021/la302974j', '10.1021/la901499x', '10.1021/la902266x', '10.1021/nl101235d', '10.1021/nl104410t', '10.1021/nl200052j', '10.1021/nl3001309', '10.1021/nl301478n', '10.1021/nl803047b', '10.1021/nn101260f', '10.1021/nn204190e', '10.1021/nn204398m', '10.1021/nn2048153', '10.1021/nn303144r', '10.1021/nn901310k', '10.1021/np1009493', '10.1021/np2005055', '10.1021/ol202800k', '10.1029/2008JF001186', '10.1029/2009JA015100', '10.1038/ncomms1441', '10.1038/cddis.2012.39', '10.1038/emboj.2010.264', '10.1038/emboj.2011.267', '10.1038/mt.2011.105.', '10.1038/nature07934', '10.1038/nature08579', '10.1038/nature09056', '10.1038/nature09829', '10.1038/nature10095', '10.1038/nature10640', '10.1038/nbt.1646', '10.1038/ncb2091', '10.1038/ncb2465', '10.1038/nchembio.688', '10.1038/NCHEM.1111', '10.1038/ncomms1585', '10.1038/ng.2007.45', '10.1038/ng.790', '10.1038/ni.1905', '10.1038/nmeth.f.308', '10.1038/nmeth.1763', '10.1038/nm.2058', '10.1038/nm.2127', '10.1038/nm.2127', '10.1038/nm.2470', '10.1038/nm.2600', '10.1038/nm.2966', '10.1038/nphys2159', '10.1038/nrm3394', '10.1038/nsmb.1897', '10.1038/onc.2010.636', '10.1039/b905270d', '10.1039/b925367j', '10.1039/b926284a', '10.1039/C0CC02573A', '10.1039/c0cc04641h', '10.1039/c0cs00111b', '10.1039/C0LC00716A', '10.1039/C0PP00159G', '10.1039/C0SC00329H', '10.1039/C0SC00495B', '10.1039/C0SC00523A', '10.1039/c0sm00610f', '10.1039/C000977F', '10.1039/c003758c', '10.1039/c003908j', '10.1039/c004787m', '10.1039/C005485M', '10.1039/C1CC11167A', '10.1039/C1CC11206F', '10.1039/c1cp23298c', '10.1039/C1DT10667H', '10.1039/C1DT10820D', '10.1039/C1DT11254F', '10.1039/C1EE01254A', '10.1039/C1NR11274K', '10.1039/c1ob05097d', '10.1039/C1OB06126G', '10.1039/c1sc00298h', '10.1039/c1sm05407d', '10.1039/c1sm05602f', '10.1039/c1sm05795b', '10.1039/C2AN35207A', '10.1039/C2CC31533E', '10.1039/c2cp23070d', '10.1039/c2cp23931k', '10.1039/c2cp40175D', '10.1039/C2CY20405C', '10.1039/C2DT11861K', '10.1039/C2DT12250B', '10.1039/C2JM15716K', '10.1039/C2LC21279J', '10.1039/C2NR11817C', '10.1039/c2nr30605k', '10.1039/C2OB06717J', '10.1039/C2RA20192E', '10.1039/c2sc01064j', '10.1042/AN20110061', '10.1042/AN20110061', '10.1042/BST0361313', '10.1051/medsci/200622141', '10.1051/0004-6361/200811481', '10.1051/0004-6361/200912399', '10.1051/0004-6361/200913121', '10.1051/0004-6361/201015862', '10.1051/0004-6361/201016098', '10.1051/0004-6361/201116681', '10.1051/0004-6361/201118235', '10.1051/0004-6361/201218970', '10.1053/j.gastro.2008.01.035', '10.1055/s-0031-1286316', '10.1055/s-0031-1290588', '10.1061/(ASCE)GT.1943-5606.0000182', '10.1063/1.3464464', '10.1063/1.3505095', '10.1063/1.3534078', '10.1063/1.3569146', '10.1063/1.3615070', '10.1063/1.3630123', '10.1063/1.3640045', '10.1063/1.3652912', '10.1073/pnas.0405398101', '10.1073/pnas.0813160106', '10.1073/pnas.0910371106', '10.1073/pnas.1004562107', '10.1073/pnas.1009719107', '10.1073/pnas.1010018107', '10.1073/pnas.1010647108', '10.1073/pnas.1112708109', '10.1073/pnas.1201079109', '10.1073/pnas.1201371109', '10.1080/0731129X.2011.559057', '10.1080/15376494.2010.528155', '10.1080/15732471003588437', '10.1080/19443994.2012.677516', '10.1080/19648189.2011.9695304', '10.1084/jem.20101757', '10.1086/605911', '10.1086/648598', '10.1086/661906', '10.1088/0004-637X/707/2/L128', '10.1088/0004-637X/734/1/55', '10.1088/0004-637X/743/2/164', '10.1088/0004-637X/744/1/10', '10.1088/0004-637X/744/1/11', '10.1088/0004-637X/752/2/155', '10.1088/0264-9381/28/7/075013', '10.1088/0953-4075/45/7/074006', '10.1088/0953-8984/23/13/133001', '10.1088/0957-4484/21/46/465203', '10.1088/0957-4484/23/29/294003', '10.1088/1126-6708/2009/05/074', '10.1088/1367-2630/11/8/083029', '10.1088/1367-2630/13/7/073014', '10.1088/1367-2630/14/8/085019', '10.1088/1475-7516/2012/08/029', '10.1088/1751-8113/44/30/305404', '10.1088/2041-8205/742/2/L18', '10.1089/ars.2010.3841', '10.1089/ars.2010.3852', '10.1089/ars.2010.3859', '10.1091/mbc.E05-04-0304', '10.1093/bioinformatics/btr043', '10.1093/brain/awr032', '10.1093/cercor/bhs122', '10.1093/cvr/cvq318', '10.1093/database/bar040', '10.1093/gerona/gls119', '10.1093/glycob/cwp067', '10.1093/glycob/cwq169', '10.1093/glycob/cwq176', '10.1093/glycob/cwq179', '10.1093/hmg/ddl074', '10.1093/hmg/ddm263', '10.1093/hmg/ddn379', '10.1093/hmg/ddp262', '10.1093/icc/dtr005', '10.1093/imrn/rnq186', '10.1093/imrn/rnr202', '10.1093/nar/gkl1021', '10.1093/nar/gkn1058', '10.1093/nar/gkq431', '10.1093/nar/gkq692', '10.1093/nar/gkr991', '10.1093/rheumatology/keq029v1', '10.1093/rheumatology/keq338v1', '10.1095/biolreprod.111.091892', '10.1097/NEN.0b013e31819385fd', '10.1098/rsfs.2010.0038', '10.1098/rspa.2011.0680', '10.1098/rstb.2009.0313', '10.1101/gr.116764.110', '10.1103/PhysRevA.82.063812', '10.1103/PhysRevA.85.013823', '10.1103/PhysRevA.86.041602', '10.1103/PhysRevB.82.121303', '10.1103/PhysRevB.85.075441', '10.1103/PhysRevB.85.165148', '10.1103/PhysRevB.86.035402', '10.1103/PhysRevD.83.014505', '10.1103/PhysRevD.83.045010', '10.1103/PhysRevD.83.094502', '10.1103/PhysRevD.83.095003', '10.1103/PhysRevD.83.114513', '10.1103/PhysRevD.84.035010', '10.1103/PhysRevD.84.035028', '10.1103/PhysRevD.84.085007', '10.1103/PhysRevD.85.055026', '10.1103/PhysRevD.85.086010', '10.1103/PhysRevD.85.115002', '10.1103/PhysRevD.86.035015', '10.1103/PhysRevLett.102.117002', '10.1103/PhysRevLett.102.127401', '10.1103/PhysRevLett.102.191301', '10.1103/PhysRevLett.104.221801', '10.1103/PhysRevLett.105.233001', '10.1103/PhysRevLett.105.257601', '10.1103/PhysRevLett.105.266807', '10.1103/PhysRevLett.106.056101', '10.1103/PhysRevLett.106.193009', '10.1103/PhysRevLett.107.116101', '10.1103/PhysRevLett.107.133002', '10.1103/PhysRevLett.108.106802', '10.1103/PhysRevLett.108.193005', '10.1103/PhysRevLett.109.075302', '10.1103/PhysRevX.2.011005', '10.1104/pp.111.175737', '10.1105/tpc.112.099861', '10.1107/S160053681003895X', '10.1108/S1048-4736(2010)0000021004', '10.1108/03321641211227357', '10.1109/COMPSAC.2011.66', '10.1109/CSMR.2011.49', '10.1109/DASC.2011.6096119', '10.1109/DASC.2011.6096120', '10.1109/DSD.2011.41', '10.1109/DSN.2011.5958214', '10.1109/EMBC.2012.6346934', '10.1109/EuCAP.2012.6205956', '10.1109/EXPRES.2011.5741805', '10.1109/ICEAA.2011.6046423', '10.1109/ICLP.2012.6344412', '10.1109/ICLP.2012.6344413', '10.1109/ICTEL.2009.5158658', '10.1109/IEMBS.2011.6091748', '10.1109/ISPLC.2009.4913404', '10.1109/ISPLC.2010.5479921', '10.1109/ISPLC.2011.5764398', '10.1109/IST.2012.6295545', '10.1109/ITAB.2010.5687680', '10.1109/IWBE.2011.6079023', '10.1109/IWBP.2011.5954857', '10.1109/JPHOT.2011.2127469', '10.1109/LGRS.2011.2109934', '10.1109/OPTIM.2010.5510360', '10.1109/OPTIM.2010.5510442', '10.1109/OPTIM.2010.5510562', '10.1109/OPTIM.2010.5510564', '10.1109/OPTIM.2010.5510567', '10.1109/OPTIM.2010.5510578', '10.1109/SPLC.2011.52', '10.1109/TEMC.2011.2149533', '10.1109/TGRS.2011.2168962', '10.1109/WCRE.2011.45', '10.1111/j.1349-7006.2009.01223.x', '10.1111/j.1365-2141.2012.09222.x', '10.1111/j.1365-2362.2010.02335', '10.1111/j.1365-2435.2010.01776.x', '10.1111/j.1365-2664.2009.01716.x', '10.1111/j.1365-2664.2010.01854.x', '10.1111/j.1365-2664.2011.02022.x', '10.1111/j.1365-2699.2011.02663.x', '10.1111/j.1365-2796.2011.02431.x.', '10.1111/j.1365-2958.2009.06633.x', '10.1111/j.1365-2958.2009.06838.x', '10.1111/j.1365-2966.2011.19370.x', '10.1111/j.1365-2966.2011.20104.x', '10.1111/j.1365-2982.2009.01362x', '10.1111/j.1365-2990.2008.00996.x', '10.1111/j.1460-9568.2010.07122.x', '10.1111/j.1460-9568.2010.07281.x', '10.1111/j.1460-9568.2011.07645.x.', '10.1111/j.1461-0248.2011.01697.x', '10.1111/j.1462-5822.2011.01631.x', '10.1111/j.1465-7287.2009.00186.x', '10.1111/j.1471-4159.2009.06266.x', '10.1111/j.1476-5381.2011.01468.x.', '10.1111/j.1523-1739.2008.01158.x', '10.1111/j.1523-1739.2010.01598.x', '10.1111/j.1523-1739.2010.01605.x', '10.1111/j.1528-1167.2009.02472.x', '10.1111/j.1528-1167.2010.02547.x', '10.1111/j.1528-1167.2010.02678.x', '10.1111/j.1528-1167.2011.03033.x', '10.1111/j.1528-1167.2011.03073.x', '10.1111/j.1528-1167.2011.03115.x.', '10.1111/j.1528-1167.2011.03242.x', '10.1111/j.1528-1167.2011.03306.x.', '10.1111/j.1528-1167.2012.03513.x', '10.1111/j.1540-6520.2010.00411.x', '10.1111/j.1574-6968.2010.02030.x', '10.1111/j.1574-6968.2010.02030.x', '10.1111/j.1574-6968.2012.02517.x', '10.1111/j.1582-4934.2008.00499.x', '10.1111/j.1742-4658.2009.07134.x', '10.1111/j.1750-3639.2009.00341.x', '10.1111/j.1939-7445.2011.00108.x', '10.1111/j.2041-210X.2012.00196.x', '10.1112/plms/pdr069', '10.1112/S0010437X09004163', '10.1113/jphysiol.2008.167155', '10.1113/jphysiol.2009.180570', '10.1117/12.908604', '10.1126/science.1172740', '10.1126/science.1175509', '10.1126/science.1176495', '10.1126/science.1187420', '10.1126/science.1195253', '10.1126/science.1212525', '10.1126/scitranslmed.3002922', '10.1128/AEM.02326-10', '10.1128/JCM.01891-10', '10.1128/mBio.00250-11', '10.1134/S0021364011230081', '10.1134/S0037446606010174', '10.1136/jmg.2008.060541', '10.1142/S0218271811020652', '10.1142/S2010194512005053', '10.1145/1950413.1950464', '10.1145/2019136.2019169', '10.1145/2025113.2025189', '10.1145/2110147.2110158', '10.1145/2351676.2351730', '10.1146/annurev.micro.091208.073507', '10.1149/2.062211jes', '10.1155/JBB/2006/64347', '10.1155/2009/453471', '10.1158/1535-7163.MCT-11-0100', '10.1161/CIRCRESAHA.111.250738', '10.1162/jocn_a_00049', '10.1172/JCI57813', '10.1177/1350508412452623', '10.1179/030801811X13013181961301', '10.1182/blood-2009-07-229450', '10.1182/blood-2009-10-247361', '10.1182/blood-2009-10-248211', '10.1186/ar3168v1', '10.1186/1471-2164-10-302', '10.1186/1471-2180-10-141', '10.1186/1471-2202-11-11', '10.1209/0295-5075/97/24004', '10.1242/dev.041632', '10.1242/jcs.051862', '10.1242/jeb.051664', '10.1364/AO.51.007160', '10.1364/JOSAB.29.00A127', '10.1364/OE.19.001617', '10.1364/OE.20.000426', '10.1364/OL.37.000100', '10.1371/annotation/4ec9cbbd-7620-4449-8961-28213e9dadf4', '10.1371/journal.pbio.1000016', '10.1371/journal.pbio.1000352', '10.1371/journal.pbio.1001259', '10.1371/journal.pone.0005976', '10.1371/journal.pone.0007663', '10.1371/journal.pone.0015693', '10.1371/journal.pone.0016342', '10.1371/journal.pone.0017575.g002', '10.1371/journal.pone.0017686', '10.1371/journal.pone.0018839', '10.1371/journal.pone.0019109', '10.1371/journal.pone.0019747', '10.1371/journal.pone.0020893', '10.1371/journal.pone.0027575', '10.1371/journal.pone.0028549', '10.1371/journal.pone.0028808', '10.1371/journal.pone.0032604', '10.1371/journal.pone.0033654', '10.1371/journal.pone.0035233', '10.1371/journal.pone.0042305', '10.1371/journal.pone.0043835', '10.1371/journal.ppat.1000518', '10.1371/journal.ppat.1002692', '10.1371/journal.ppat.1002875', '10.1512/iumj.2010.59.4237', '10.1523/JNEUROSCI.0392-12.2012', '10.1523/JNEUROSCI.3790-08.2009', '10.1557/opl.2012.723', '10.1586/ERM.11.90', '10.2007/s10961-007-9065-8', '10.2007/s11187-007-9071-0', '10.2134/agronj2011.0101', '10.2147/CHC.S5792', '10.2353/ajpath.2008.070830', '10.2533/chimia.2010.826', '10.3152/030234210X508615', '10.3152/030234210X508633', '10.3152/030234210X508642', '10.3166/ejece.14.11-28', '10.3233/978-1-60750-604-1-621', '10.3354/esr00274', '10.3389/conf.fnhum.2011.207.00332', '10.3389/conf.fnhum.2011.207.00342', '10.3389/fimmu.2012.00236', '10.3389/fncel.2011.00008', '10.3389/fncir.2010.00126', '10.3390/md10010051', '10.3390/md9020242', '10.3390/md9061157', '10.3390/md9122809', '10.3390/mi3020218', '10.3390/molecules16108694', '10.3390/s110707063', '10.3762/bjoc.8.60', '10.3762/bjoc.8.85', '10.3892/ijo.2011', '10.4161/gmic.19182', '10.4161/nucl.18930', '10.4171/CMH/249', '10.4230/LIPIcs.FSTTCS.2011.127', '10.4230/LIPIcs.STACS.2011.543', '10.5004/dwt.2011.2334', '10.5004/dwt.2011.3130', '10.5004/dwt.2012.2456', '10.5194/nhess-10-2055-2010', '10.5194/nhess-12-615-2012', '10.5194/nhess-9-1059-2009', '10.5465/armr.2009.0358', '10.7305/automatika.53-1.139'
]
'''

list_DOIs = ['10.1016/j.bbadis.2008.10.020', '10.1016/j.semcdb.2010.01.009', '10.1016/j.jneumeth.2010.12.021', '10.1016/j.respol.2010.05.014', '10.1038/mt.2011.105', '10.1093/rheumatology/keq029', '10.1093/rheumatology/keq338', '10.1111/j.1365-2362.2010.02335.x', '10.1111/j.1365-2796.2011.02431.x', '10.1111/j.1365-2982.2009.01362.x', '10.1111/j.1460-9568.2011.07645.x', '10.1111/j.1476-5381.2011.01468.x', '10.1111/j.1528-1167.2011.03115.x', '10.1111/j.1528-1167.2011.03306.x', '10.1186/ar3168', '10.1371/journal.pone.0017575', '10.3233/978-1-60750-604-1-621', '10.4230/LIPIcs.FSTTCS.2011.127']



def saveJournalData(tree, DOI_Nbr, DOI):
    record = {}
    record['Nbr'] = DOI_Nbr
    record['DOI'] = DOI
    record['Type'] = 'Journal'

    # Journal Title 
    if len(tree.xpath("/doi_records/doi_record/crossref/journal/journal_metadata/full_title/text()")):
        record['title'] = tree.xpath("/doi_records/doi_record/crossref/journal/journal_metadata/full_title/text()")[0].strip();

    # Journal Title abbreviation
    if len(tree.xpath("/doi_records/doi_record/crossref/journal/journal_metadata/abbrev_title")):
        record['abbrev_title'] = tree.xpath("/doi_records/doi_record/crossref/journal/journal_metadata/abbrev_title/text()")[0].strip();

    # ISSN
    if len(tree.xpath("/doi_records/doi_record/crossref/journal/journal_metadata/issn[@media_type='print']")):
        record['issn'] = tree.xpath("/doi_records/doi_record/crossref/journal/journal_metadata/issn[@media_type='print']/text()")[0].strip();
    else:
        record['issn'] = tree.xpath("/doi_records/doi_record/crossref/journal/journal_metadata/issn/text()")

    # eISSN
    if len(tree.xpath("/doi_records/doi_record/crossref/journal/journal_metadata/issn[@media_type='electronic']")):
        record['eissn'] = tree.xpath("/doi_records/doi_record/crossref/journal/journal_metadata/issn[@media_type='electronic']/text()")[0].strip();

    # Publication Date 'print'
    if len(tree.xpath("/doi_records/doi_record/crossref/journal/journal_issue/publication_date[@media_type='print']/day")):
        record['printPublicationDate_Day'] = tree.xpath("/doi_records/doi_record/crossref/journal/journal_issue/publication_date[@media_type='print']/day/text()")[0].strip();

    if len(tree.xpath("/doi_records/doi_record/crossref/journal/journal_issue/publication_date[@media_type='print']/month")):
        record['printPublicationDate_Month'] = tree.xpath("/doi_records/doi_record/crossref/journal/journal_issue/publication_date[@media_type='print']/month/text()")[0].strip();

    if len(tree.xpath("/doi_records/doi_record/crossref/journal/journal_issue/publication_date[@media_type='print']/year")):
        record['printPublicationDate_Year'] = tree.xpath("/doi_records/doi_record/crossref/journal/journal_issue/publication_date[@media_type='print']/year/text()")[0].strip();

    # Publication Date 'online'
    if len(tree.xpath("/doi_records/doi_record/crossref/journal/journal_issue/publication_date[@media_type='online']/day")):
        record['onlinePublicationDate_Day'] = tree.xpath("/doi_records/doi_record/crossref/journal/journal_issue/publication_date[@media_type='online']/day/text()")[0].strip();

    if len(tree.xpath("/doi_records/doi_record/crossref/journal/journal_issue/publication_date[@media_type='online']/month")):
        record['onlinePublicationDate_Month'] = tree.xpath("/doi_records/doi_record/crossref/journal/journal_issue/publication_date[@media_type='online']/month/text()")[0].strip();

    if len(tree.xpath("/doi_records/doi_record/crossref/journal/journal_issue/publication_date[@media_type='online']/year")):
        record['onlinePublicationDate_Year'] = tree.xpath("/doi_records/doi_record/crossref/journal/journal_issue/publication_date[@media_type='online']/year/text()")[0].strip();

    # Journal Volume
    if len(tree.xpath("/doi_records/doi_record/crossref/journal/journal_issue/journal_volume/volume/text()")):
        record['journal_volume'] = tree.xpath("/doi_records/doi_record/crossref/journal/journal_issue/journal_volume/volume/text()")[0].strip();
    
    # Journal Issue
    if len(tree.xpath("/doi_records/doi_record/crossref/journal/journal_issue/issue/text()")):
        record['journal_issue'] = tree.xpath("/doi_records/doi_record/crossref/journal/journal_issue/issue/text()")[0].strip();
    
    # Article Title
    if len(tree.xpath("/doi_records/doi_record/crossref/journal/journal_article/titles/title/text()")):
        record['article_title'] = tree.xpath("/doi_records/doi_record/crossref/journal/journal_article/titles/title/text()")[0].strip();

    # Article Title (full text)
    if len(tree.xpath("/doi_records/doi_record/crossref/journal/journal_article[@publication_type='full_text']/titles/title/text()")):
        record['article_title_full'] = tree.xpath("/doi_records/doi_record/crossref/journal/journal_article[@publication_type='full_text']/titles/title/text()")[0].strip();

    # Pages
    if len(tree.xpath("/doi_records/doi_record/crossref/journal/journal_article/pages/first_page/text()")):
        record['first_page'] = tree.xpath("/doi_records/doi_record/crossref/journal/journal_article/pages/first_page/text()")[0].strip();

    if len(tree.xpath("/doi_records/doi_record/crossref/journal/journal_article/pages/last_page/text()")):
        record['last_page'] = tree.xpath("/doi_records/doi_record/crossref/journal/journal_article/pages/last_page/text()")[0].strip();

    # Print out the data we've gathered
    print record
    # Finally, save the record to the datastore - 'Nr' is our unique key
    scraperwiki.sqlite.save(["Nbr"], record)

def saveBookData(tree, DOI_Nbr, DOI):
    record = {}
    record['Nbr'] = DOI_Nbr
    record['DOI'] = DOI
    if len(tree.xpath("/doi_records/doi_record/crossref/book/book_series_metadata/text()")):
        fillBookSeriesData(record)

    if len(tree.xpath("/doi_records/doi_record/crossref/book/book_metadata/text()")):
        fillBookData(record)
        
    # Print out the data we've gathered
    print record
    # Finally, save the record to the datastore - 'Nr' is our unique key
    scraperwiki.sqlite.save(["Nbr"], record)

def fillBookSeriesData(record):
    record['Type'] = 'BookSeries'

    # BookSeries Title
    if len(tree.xpath("/doi_records/doi_record/crossref/book/book_series_metadata/titles/title/text()")):
        record['title'] = tree.xpath("/doi_records/doi_record/crossref/book/book_series_metadata/titles/title/text()")[0].strip();

    # ISSN
    if len(tree.xpath("/doi_records/doi_record/crossref/book/book_series_metadata/issn[@media_type='print']")):
        record['issn'] = tree.xpath("/doi_records/doi_record/crossref/book/book_series_metadata/issn[@media_type='print']/text()")[0].strip();

    # eISSN
    if len(tree.xpath("/doi_records/doi_record/crossref/book/book_series_metadata/issn[@media_type='electronic']")):
        record['eissn'] = tree.xpath("/doi_records/doi_record/crossref/book/book_series_metadata/issn[@media_type='electronic']/text()")[0].strip();

    # isbn 'print'
    if len(tree.xpath("/doi_records/doi_record/crossref/book/book_series_metadata/isbn[@media_type='print']")):
        record['isbnPrint'] = tree.xpath("/doi_records/doi_record/crossref/book/book_series_metadata/isbn[@media_type='print']/text()")[0].strip();

    # isbn 'online'
    if len(tree.xpath("/doi_records/doi_record/crossref/book/book_series_metadata/isbn[@media_type='online']")):
        record['isbnOnline'] = tree.xpath("/doi_records/doi_record/crossref/book/book_series_metadata/isbn[@media_type='online']/text()")[0].strip();


    # Publication Date 'print'
    if len(tree.xpath("/doi_records/doi_record/crossref/book/book_series_metadata/publication_date[@media_type='print']/day")):
        record['printPublicationDate_Day'] = tree.xpath("/doi_records/doi_record/crossref/book/book_series_metadata/publication_date[@media_type='print']/day/text()")[0].strip();

    if len(tree.xpath("/doi_records/doi_record/crossref/book/book_series_metadata/publication_date[@media_type='print']/month")):
        record['printPublicationDate_Month'] = tree.xpath("/doi_records/doi_record/crossref/book/book_series_metadata/publication_date[@media_type='print']/month/text()")[0].strip();

    if len(tree.xpath("/doi_records/doi_record/crossref/book/book_series_metadata/publication_date[@media_type='print']/year")):
        record['printPublicationDate_Year'] = tree.xpath("/doi_records/doi_record/crossref/book/book_series_metadata/publication_date[@media_type='print']/year/text()")[0].strip();

    # Publication Date 'online'
    if len(tree.xpath("/doi_records/doi_record/crossref/book/book_series_metadata/publication_date[@media_type='online']/day")):
        record['onlinePublicationDate_Day'] = tree.xpath("/doi_records/doi_record/crossref/book/book_series_metadata/publication_date[@media_type='online']/day/text()")[0].strip();

    if len(tree.xpath("/doi_records/doi_record/crossref/book/book_series_metadata/publication_date[@media_type='online']/month")):
        record['onlinePublicationDate_Month'] = tree.xpath("/doi_records/doi_record/crossref/book/book_series_metadata/publication_date[@media_type='online']/month/text()")[0].strip();

    if len(tree.xpath("/doi_records/doi_record/crossref/book/book_series_metadata/publication_date[@media_type='online']/year")):
        record['onlinePublicationDate_Year'] = tree.xpath("/doi_records/doi_record/crossref/book/book_series_metadata/publication_date[@media_type='online']/year/text()")[0].strip();

    # Publisher Name
    if len(tree.xpath("/doi_records/doi_record/crossref/book/book_series_metadata/publisher/publisher_name/text()")):
        record['bookseries publisher name'] = tree.xpath("/doi_records/doi_record/crossref/book/book_series_metadata/publisher/publisher_name/text()")[0].strip();

    # Publisher Place
    if len(tree.xpath("/doi_records/doi_record/crossref/book/book_series_metadata/publisher/publisher_place/text()")):
        record['bookseries publisher place'] = tree.xpath("/doi_records/doi_record/crossref/book/book_series_metadata/publisher/publisher_place/text()")[0].strip();

    # Chapter Title
    if len(tree.xpath("/doi_records/doi_record/crossref/book/content_item/titles/title/text()")):
        record['bookseries chapter title'] = tree.xpath("/doi_records/doi_record/crossref/book/content_item/titles/title/text()")[0].strip();
    
    # Pages
    if len(tree.xpath("/doi_records/doi_record/crossref/crossref/book/content_item/pages/first_page/text()")):
        record['first_page'] = tree.xpath("/doi_records/doi_record/crossref/crossref/book/content_item/pages/first_page/text()")[0].strip();
    if len(tree.xpath("/doi_records/doi_record/crossref/crossref/book/content_item/pages/last_page/text()")):
        record['last_page'] = tree.xpath("/doi_records/doi_record/crossref/crossref/book/content_item/pages/last_page/text()")[0].strip();

def fillBookData(record):
    record['Type'] = 'Book'

    # Book Title
    if len(tree.xpath("/doi_records/doi_record/crossref/book/book_metadata/titles/title/text()")):
        record['title'] = tree.xpath("/doi_records/doi_record/crossref/book/book_metadata/titles/title/text()")[0].strip();

    # Book Subtitle
    if len(tree.xpath("/doi_records/doi_record/crossref/book/book_metadata/titles/subtitle/text()")):
        record['subtitle'] = tree.xpath("/doi_records/doi_record/crossref/book/book_metadata/titles/subtitle/text()")[0].strip();

    # Publication Date 'print'
    if len(tree.xpath("/doi_records/doi_record/crossref/book/book_metadata/publication_date[@media_type='print']/day")):
        record['printPublicationDate_Day'] = tree.xpath("/doi_records/doi_record/crossref/book/book_metadata/publication_date[@media_type='print']/day/text()")[0].strip();

    if len(tree.xpath("/doi_records/doi_record/crossref/book/book_metadata/publication_date[@media_type='print']/month")):
        record['printPublicationDate_Month'] = tree.xpath("/doi_records/doi_record/crossref/book/book_metadata/publication_date[@media_type='print']/month/text()")[0].strip();

    if len(tree.xpath("/doi_records/doi_record/crossref/book/book_metadata/publication_date[@media_type='print']/year")):
        record['printPublicationDate_Year'] = tree.xpath("/doi_records/doi_record/crossref/book/book_metadata/publication_date[@media_type='print']/year/text()")[0].strip();

    # Publication Date 'online'
    if len(tree.xpath("/doi_records/doi_record/crossref/book/book_metadata/publication_date[@media_type='online']/day")):
        record['onlinePublicationDate_Day'] = tree.xpath("/doi_records/doi_record/crossref/book/book_metadata/publication_date[@media_type='online']/day/text()")[0].strip();

    if len(tree.xpath("/doi_records/doi_record/crossref/book/book_metadata/publication_date[@media_type='online']/month")):
        record['onlinePublicationDate_Month'] = tree.xpath("/doi_records/doi_record/crossref/book/book_metadata/publication_date[@media_type='online']/month/text()")[0].strip();

    if len(tree.xpath("/doi_records/doi_record/crossref/book/book_metadata/publication_date[@media_type='online']/year")):
        record['onlinePublicationDate_Year'] = tree.xpath("/doi_records/doi_record/crossref/book/book_metadata/publication_date[@media_type='online']/year/text()")[0].strip();
    
    # isbn 'print'
    if len(tree.xpath("/doi_records/doi_record/crossref/book/book_metadata/isbn[@media_type='print']")):
        record['isbnPrint'] = tree.xpath("/doi_records/doi_record/crossref/book/book_metadata/isbn[@media_type='print']/text()")[0].strip();

    # isbn 'online'
    if len(tree.xpath("/doi_records/doi_record/crossref/book/book_metadata/isbn[@media_type='online']")):
        record['isbnOnline'] = tree.xpath("/doi_records/doi_record/crossref/book/book_metadata/isbn[@media_type='online']/text()")[0].strip();

    # Publisher Name
    if len(tree.xpath("/doi_records/doi_record/crossref/book/book_metadata/publisher/publisher_name/text()")):
        record['book publisher name'] = tree.xpath("/doi_records/doi_record/crossref/book/book_metadata/publisher/publisher_name/text()")[0].strip();
    
    # Article Title
    if len(tree.xpath("/doi_records/doi_record/crossref/book/content_item/titles/title/text()")):
        record['article_title'] = tree.xpath("/doi_records/doi_record/crossref/book/content_item/titles/title/text()")[0].strip();

    # Pages
    if len(tree.xpath("/doi_records/doi_record/crossref/crossref/book/content_item/pages/first_page/text()")):
        record['first_page'] = tree.xpath("/doi_records/doi_record/crossref/crossref/book/content_item/pages/first_page/text()")[0].strip();
    if len(tree.xpath("/doi_records/doi_record/crossref/crossref/book/content_item/pages/last_page/text()")):
        record['last_page'] = tree.xpath("/doi_records/doi_record/crossref/crossref/book/content_item/pages/last_page/text()")[0].strip();


def saveConferenceData(tree, DOI_Nbr, DOI):
    record = {}
    record['Nbr'] = DOI_Nbr
    record['DOI'] = DOI
    record['Type'] = 'Conference'
    
    # Conference proceedings Title
    if len(tree.xpath("/doi_records/doi_record/crossref/conference/proceedings_metadata/proceedings_title/text()")):
        record['title'] = tree.xpath("/doi_records/doi_record/crossref/conference/proceedings_metadata/proceedings_title/text()")[0].strip();
    
    # Publisher name 
    if len(tree.xpath("/doi_records/doi_record/crossref/conference/proceedings_metadata/publisher/publisher_name/text()")):
        record['bookseries publisher name'] = tree.xpath("/doi_records/doi_record/crossref/conference/proceedings_metadata/publisher/publisher_name/text()")[0].strip();

    # Publication Date
    if len(tree.xpath("/doi_records/doi_record/crossref/conference/proceedings_metadata/publication_date/day")):
        record['PublicationDate_Day'] = tree.xpath("/doi_records/doi_record/crossref/conference/proceedings_metadata/publication_date/day/text()")[0].strip();

    if len(tree.xpath("/doi_records/doi_record/crossref/conference/proceedings_metadata/publication_date/month")):
        record['PublicationDate_Month'] = tree.xpath("/doi_records/doi_record/crossref/conference/proceedings_metadata/publication_date/month/text()")[0].strip();

    if len(tree.xpath("/doi_records/doi_record/crossref/conference/proceedings_metadata/publication_date/year")):
        record['PublicationDate_Year'] = tree.xpath("/doi_records/doi_record/crossref/conference/proceedings_metadata/publication_date/year/text()")[0].strip();

    # isbn 'print'
    if len(tree.xpath("/doi_records/doi_record/crossref/conference/proceedings_metadata/isbn[@media_type='print']")):
        record['isbnPrint'] = tree.xpath("/doi_records/doi_record/crossref/conference/proceedings_metadata/isbn[@media_type='print']/text()")[0].strip();

    # isbn 'online'
    if len(tree.xpath("/doi_records/doi_record/crossref/conference/proceedings_metadata/isbn[@media_type='online']")):
        record['isbnOnline'] = tree.xpath("/doi_records/doi_record/crossref/conference/proceedings_metadata/isbn[@media_type='online']/text()")[0].strip();

    # Article Title
    if len(tree.xpath("/doi_records/doi_record/crossref/conference/conference_paper/titles/title/text()")):
        record['article_title'] = tree.xpath("/doi_records/doi_record/crossref/conference/conference_paper/titles/title/text()")[0].strip();

    # Pages
    if len(tree.xpath("/doi_records/doi_record/crossref/conference/conference_paper/pages/first_page/text()")):
        record['first_page'] = tree.xpath("/doi_records/doi_record/crossref/conference/conference_paper/pages/first_page/text()")[0].strip();
    if len(tree.xpath("/doi_records/doi_record/crossref/conference/conference_paper/pages/last_page/text()")):
        record['last_page'] = tree.xpath("/doi_records/doi_record/crossref/conference/conference_paper/pages/last_page/text()")[0].strip();


    # Print out the data we've gathered
    print record
    # Finally, save the record to the datastore - 'Nr' is our unique key
    scraperwiki.sqlite.save(["Nbr"], record)


def saveUnknown(DOI_Nbr, DOI):
    record = {}
    record['Nbr'] = DOI_Nbr
    record['DOI'] = DOI
    record['Type'] = 'Unknown'
    
        

    # Print out the data we've gathered
    print record
    # Finally, save the record to the datastore - 'Nr' is our unique key
    scraperwiki.sqlite.save(["Nbr"], record)

'''
list_DOIs = ['10.1002/hep.24509', '10.1007/JHEP11(2010)119', '10.1104/pp.112.200303', '10.1007/978-3-642-34234-9_21', '10.1007/978-3-642-34234-9_34', '10.1016/j.tcb.2009.11.004', '10.1073/pnas.1010833108', '10.1103/PhysRevA.84.013603', '10.1103/PhysRevA.85.043401', '10.1103/PhysRevLett.105.153604', '10.1128/MCB.01500-09', '10.1140/epjd/e2011-20071-x', '10.1182/blood-2010-10-313643', '10.1209/0295-5075/98/30005', '10.2337/dc09-0324', '10.1002/anie.201108849', '10.1002/cbic.201100282', '10.1007/JHEP01(2011)030', '10.1007/JHEP01(2012)006', '10.1007/JHEP05(2011)003', '10.1007/JHEP10(2010)042', '10.1021/am200811c', '10.1073/pnas.1120774109', '10.1088/1126-6708/2009/08/092', '10.1088/1126-6708/2009/10/030', '10.1088/1126-6708/2009/10/032', '10.1111/j.1742-4658.2010.07867.x', '10.1201/b11279-22', '10.1016/j.bmcl.2011.08.057', '10.1016/j.cell.2009.01.049', '10.1016/j.drudis.2011.06.003', '10.1016/j.jbiomech.2012.05.019', '10.1016/j.jtbi.2010.10.025', '10.1029/2009JC006087', '10.1038/nature10196', '10.1038/onc.2011.519', '10.1088/0004-637X/721/1/777', '10.1088/0004-637X/724/2/1396', '10.1088/0004-637X/727/1/15', '10.1088/0004-637X/736/2/159']
'''

counter = 0;

for DOI in list_DOIs:
    xml = scraperwiki.scrape("http://www.crossref.org/openurl/?id=" + DOI + "&noredirect=true&pid=RTD-CORDA-SUPPORT@ec.europa.eu&format=unixref")
    tree = et.fromstring(xml, et.XMLParser(encoding="utf-8"))
    
    typeDOI = tree.xpath("/doi_records/doi_record/crossref")[0][0].tag
    counter = counter + 1;
    
    if typeDOI == 'journal':
        saveJournalData(tree, counter, DOI)
    elif typeDOI == 'book':
        saveBookData(tree, counter, DOI)
    elif typeDOI == 'conference':
        saveConferenceData(tree, counter, DOI)
    else: 
        saveUnknown(counter, DOI)


