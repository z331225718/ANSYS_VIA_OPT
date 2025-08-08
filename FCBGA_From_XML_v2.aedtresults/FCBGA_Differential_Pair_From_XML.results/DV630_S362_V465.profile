$begin 'Profile'
	$begin 'ProfileGroup'
		MajorVer=2025
		MinorVer=2
		Name='Solution Process'
		$begin 'StartInfo'
			I(1, 'Start Time', '08/07/2025 15:40:51')
			I(1, 'Host', 'ZZMJAY')
			I(1, 'Processor', '16')
			I(1, 'OS', 'NT 10.0')
			I(1, 'Product', 'HFSS Version 2025.2.0')
		$end 'StartInfo'
		$begin 'TotalInfo'
			I(1, 'Elapsed Time', '00:01:36')
			I(1, 'ComEngine Memory', '96.1 M')
		$end 'TotalInfo'
		GroupOptions=8
		TaskDataOptions('CPU Time'=8, Memory=8, 'Real Time'=8)
		ProfileItem('', 0, 0, 0, 0, 0, 'I(1, 1, \'Executing From\', \'C:\\\\Software\\\\ANSYS Inc\\\\v252\\\\AnsysEM\\\\HFSSCOMENGINE.exe\')', false, true)
		$begin 'ProfileGroup'
			MajorVer=2025
			MinorVer=2
			Name='HPC'
			$begin 'StartInfo'
				I(1, 'Type', 'Auto')
				I(1, 'MPI Vendor', 'Intel')
				I(1, 'MPI Version', '2021')
			$end 'StartInfo'
			$begin 'TotalInfo'
				I(0, ' ')
			$end 'TotalInfo'
			GroupOptions=0
			TaskDataOptions(Memory=8)
			ProfileItem('Machine', 0, 0, 0, 0, 0, 'I(5, 1, \'Name\', \'zzmjay\', 1, \'Memory\', \'29.8 GB\', 3, \'RAM Limit\', 90, \'%f%%\', 2, \'Cores\', 4, false, 1, \'Free Disk Space\', \'429 GB\')', false, true)
		$end 'ProfileGroup'
		ProfileItem('', 0, 0, 0, 0, 0, 'I(1, 1, \'Allow off core\', \'True\')', false, true)
		ProfileItem('', 0, 0, 0, 0, 0, 'I(1, 1, \'Solution Basis Order\', \'Mixed\')', false, true)
		ProfileItem('Design Validation', 0, 0, 0, 0, 0, 'I(1, 0, \'Elapsed time : 00:00:00 , HFSS ComEngine Memory : 89.2 M\')', false, true)
		ProfileItem('', 0, 0, 0, 0, 0, 'I(1, 0, \'Perform full validations with standard port validations\')', false, true)
		ProfileItem('', 0, 0, 0, 0, 0, 'I(1, 0, \'\')', false, true)
		$begin 'ProfileGroup'
			MajorVer=2025
			MinorVer=2
			Name='Initial Meshing'
			$begin 'StartInfo'
				I(1, 'Time', '08/07/2025 15:40:51')
			$end 'StartInfo'
			$begin 'TotalInfo'
				I(1, 'Elapsed Time', '00:00:23')
			$end 'TotalInfo'
			GroupOptions=4
			TaskDataOptions('CPU Time'=8, Memory=8, 'Real Time'=8)
			ProfileItem('Mesh', 18, 0, 21, 0, 137000, 'I(3, 2, \'Tetrahedra\', 61812, false, 1, \'Type\', \'TAU\', 2, \'Cores\', 4, false)', true, true)
			ProfileItem('Coarsen', 1, 0, 1, 0, 137000, 'I(1, 2, \'Tetrahedra\', 26170, false)', true, true)
			ProfileItem('Lambda Refine', 0, 0, 0, 0, 46816, 'I(1, 2, \'Tetrahedra\', 26767, false)', true, true)
			ProfileItem('Simulation Setup', 0, 0, 0, 0, 231152, 'I(2, 2, \'Tetrahedra\', 15688, false, 1, \'Disk\', \'0 Bytes\')', true, true)
			ProfileItem('Port Adapt', 0, 0, 0, 0, 244312, 'I(2, 2, \'Tetrahedra\', 15688, false, 1, \'Disk\', \'12.1 KB\')', true, true)
			ProfileItem('Port Refine', 0, 0, 0, 0, 52156, 'I(1, 2, \'Tetrahedra\', 26942, false)', true, true)
		$end 'ProfileGroup'
		$begin 'ProfileGroup'
			MajorVer=2025
			MinorVer=2
			Name='Adaptive Meshing'
			$begin 'StartInfo'
				I(1, 'Time', '08/07/2025 15:41:15')
			$end 'StartInfo'
			$begin 'TotalInfo'
				I(1, 'Elapsed Time', '00:01:11')
			$end 'TotalInfo'
			GroupOptions=4
			TaskDataOptions('CPU Time'=8, Memory=8, 'Real Time'=8)
			$begin 'ProfileGroup'
				MajorVer=2025
				MinorVer=2
				Name='Adaptive Pass 1'
				$begin 'StartInfo'
					I(1, 'Frequency', '56GHz')
				$end 'StartInfo'
				$begin 'TotalInfo'
					I(0, ' ')
				$end 'TotalInfo'
				GroupOptions=0
				TaskDataOptions('CPU Time'=8, Memory=8, 'Real Time'=8)
				ProfileItem(' ', 0, 0, 0, 0, 0, 'I(1, 0, \'\')', false, true)
				ProfileItem('Simulation Setup ', 0, 0, 0, 0, 238376, 'I(2, 2, \'Tetrahedra\', 15870, false, 1, \'Disk\', \'13.4 KB\')', true, true)
				ProfileItem('Matrix Assembly', 1, 0, 2, 0, 373600, 'I(4, 2, \'Tetrahedra\', 15870, false, 2, \'Lumped ports\', 2, false, 2, \'P1 Triangles\', 74, false, 1, \'Disk\', \'134 KB\')', true, true)
				ProfileItem('Matrix Solve', 0, 0, 3, 0, 592404, 'I(5, 1, \'Type\', \'DCS\', 2, \'Cores\', 4, false, 2, \'Matrix size\', 100263, false, 3, \'Matrix bandwidth\', 19.1908, \'%5.1f\', 1, \'Disk\', \'395 KB\')', true, true)
				ProfileItem('Field Recovery', 0, 0, 1, 0, 592404, 'I(3, 2, \'Excitations\', 4, false, 3, \'Average order\', 0.889162, \'%f\', 1, \'Disk\', \'2.38 MB\')', true, true)
				ProfileItem('Data Transfer', 0, 0, 0, 0, 96352, 'I(1, 0, \'Adaptive Pass 1\')', true, true)
				$begin 'ProfileGroup'
					MajorVer=2025
					MinorVer=2
					Name='APIPms'
					$begin 'StartInfo'
						I(1, 'Timesinceepock', '1754552478')
					$end 'StartInfo'
					$begin 'TotalInfo'
						I(0, ' ')
					$end 'TotalInfo'
					GroupOptions=16
					TaskDataOptions(Memory=8)
					ProfileItem('solverinfo', 0, 0, 0, 0, 0, 'I(10, 1, \'Solvertype\', \'shared_memory\', 1, \'Precision\', \'double\', 1, \'Solversymmetry\', \'complex_sym\', 1, \'Matrixdim\', \'100263\', 1, \'Matrixbw\', \'19.211800\', 1, \'Matrixnnz\', \'1926229\', 1, \'Rootdim\', \'297\', 1, \'Mathtype\', \'amd\', 1, \'Mpitasks\', \'1\', 1, \'Threadspertasks\', \'0\')', false, true)
					ProfileItem('sysinfo', 0, 0, 0, 0, 0, 'I(12, 1, \'Os\', \'win\', 1, \'Cpuid\', \'AMD Ryzen 9 8945HS w/ Radeon 780M Graphics\', 1, \'CpuPhysicCores\', \'8\', 1, \'CpuLogicCores\', \'16\', 1, \'Cpufreqkhz\', \'26686799872.000000\', 1, \'Cpucachelinesizebytes\', \'64\', 1, \'Cpuestlastlevelcachesizemb\', \'64.000000\', 1, \'Cpuestgflops\', \'524.799988\', 1, \'Memorybwestkbps\', \'51.200001\', 1, \'Numanodes\', \'1\', 1, \'Virtualmemkb\', \'137439000000.000000\', 1, \'Pagesizekb\', \'4096\')', false, true)
					ProfileItem('analysisinfo', 0, 0, 0, 0, 0, 'I(9, 1, \'Analysisstatus\', \'valid\', 1, \'Numsupernodes\', \'9090\', 1, \'Factornnz\', \'14375989\', 1, \'Factorestflops\', \'9808670000\', 1, \'Fbsestflops\', \'46064994\', 1, \'Rootfactestflops\', \'8734288\', 1, \'Rootfbsestflops\', \'44104\', 1, \'Analysistimesec\', \'0.363705\', 1, \'Analysismemkb\', \'54640.000000\')', false, true)
					ProfileItem('factorinfo', 0, 0, 0, 0, 0, 'I(4, 1, \'Fatorizationstatus\', \'valid\', 1, \'Factorizationnumcores\', \'4\', 1, \'Factorizationtimesec\', \'0.348020\', 1, \'Factorizationmentotalkb\', \'314174.000000\')', false, true)
					ProfileItem('fbsinfo', 0, 0, 0, 0, 0, 'I(10, 1, \'Fbstatus\', \'valid\', 1, \'Fbstype\', \'fullsolve\', 1, \'Fbsmt\', \'false\', 1, \'Fbsmrhs\', \'false\', 1, \'Fbsnumcores\', \'4\', 1, \'Fbsnumsolvestotal\', \'8\', 1, \'Fbsnumsolves\', \'5\', 1, \'Fbsavgsolvetime1solvesec\', \'0.026104\', 1, \'Fbscputimesec\', \'0.130522\', 1, \'Fbsmemorytotalkb\', \'269284.000000\')', false, true)
					ProfileItem('solverprofile', 0, 0, 0, 0, 0, 'I(2, 1, \'Maxmemkb\', \'592404\', 1, \'Maxdiskkb\', \'0\')', false, true)
				$end 'ProfileGroup'
			$end 'ProfileGroup'
			ProfileItem('', 0, 0, 0, 0, 0, 'I(1, 0, \'\')', false, true)
			$begin 'ProfileGroup'
				MajorVer=2025
				MinorVer=2
				Name='Adaptive Pass 2'
				$begin 'StartInfo'
					I(1, 'Frequency', '56GHz')
				$end 'StartInfo'
				$begin 'TotalInfo'
					I(0, ' ')
				$end 'TotalInfo'
				GroupOptions=0
				TaskDataOptions('CPU Time'=8, Memory=8, 'Real Time'=8)
				ProfileItem('Adaptive Refine', 0, 0, 0, 0, 63088, 'I(1, 2, \'Tetrahedra\', 31705, false)', true, true)
				ProfileItem(' ', 0, 0, 0, 0, 0, 'I(1, 0, \'\')', false, true)
				ProfileItem('Simulation Setup ', 0, 0, 0, 0, 248756, 'I(2, 2, \'Tetrahedra\', 20158, false, 1, \'Disk\', \'10.3 KB\')', true, true)
				ProfileItem('Matrix Assembly', 1, 0, 2, 0, 427292, 'I(4, 2, \'Tetrahedra\', 20158, false, 2, \'Lumped ports\', 2, false, 2, \'P1 Triangles\', 74, false, 1, \'Disk\', \'11 Bytes\')', true, true)
				ProfileItem('Matrix Solve', 1, 0, 4, 0, 780652, 'I(5, 1, \'Type\', \'DCS\', 2, \'Cores\', 4, false, 2, \'Matrix size\', 130268, false, 3, \'Matrix bandwidth\', 19.7169, \'%5.1f\', 1, \'Disk\', \'510 KB\')', true, true)
				ProfileItem('Field Recovery', 0, 0, 2, 0, 780652, 'I(3, 2, \'Excitations\', 4, false, 3, \'Average order\', 0.92787, \'%f\', 1, \'Disk\', \'1.26 MB\')', true, true)
				ProfileItem('Data Transfer', 0, 0, 0, 0, 96476, 'I(1, 0, \'Adaptive Pass 2\')', true, true)
				$begin 'ProfileGroup'
					MajorVer=2025
					MinorVer=2
					Name='APIPms'
					$begin 'StartInfo'
						I(1, 'Timesinceepock', '1754552485')
					$end 'StartInfo'
					$begin 'TotalInfo'
						I(0, ' ')
					$end 'TotalInfo'
					GroupOptions=16
					TaskDataOptions(Memory=8)
					ProfileItem('solverinfo', 0, 0, 0, 0, 0, 'I(10, 1, \'Solvertype\', \'shared_memory\', 1, \'Precision\', \'double\', 1, \'Solversymmetry\', \'complex_sym\', 1, \'Matrixdim\', \'130268\', 1, \'Matrixbw\', \'19.743999\', 1, \'Matrixnnz\', \'2572012\', 1, \'Rootdim\', \'525\', 1, \'Mathtype\', \'amd\', 1, \'Mpitasks\', \'1\', 1, \'Threadspertasks\', \'0\')', false, true)
					ProfileItem('sysinfo', 0, 0, 0, 0, 0, 'I(12, 1, \'Os\', \'win\', 1, \'Cpuid\', \'AMD Ryzen 9 8945HS w/ Radeon 780M Graphics\', 1, \'CpuPhysicCores\', \'8\', 1, \'CpuLogicCores\', \'16\', 1, \'Cpufreqkhz\', \'26648799232.000000\', 1, \'Cpucachelinesizebytes\', \'64\', 1, \'Cpuestlastlevelcachesizemb\', \'64.000000\', 1, \'Cpuestgflops\', \'524.799988\', 1, \'Memorybwestkbps\', \'51.200001\', 1, \'Numanodes\', \'1\', 1, \'Virtualmemkb\', \'137439000000.000000\', 1, \'Pagesizekb\', \'4096\')', false, true)
					ProfileItem('analysisinfo', 0, 0, 0, 0, 0, 'I(9, 1, \'Analysisstatus\', \'valid\', 1, \'Numsupernodes\', \'11699\', 1, \'Factornnz\', \'22743501\', 1, \'Factorestflops\', \'20324300000\', 1, \'Fbsestflops\', \'75092371\', 1, \'Rootfactestflops\', \'48237066\', 1, \'Rootfbsestflops\', \'137812\', 1, \'Analysistimesec\', \'0.586581\', 1, \'Analysismemkb\', \'72844.000000\')', false, true)
					ProfileItem('factorinfo', 0, 0, 0, 0, 0, 'I(4, 1, \'Fatorizationstatus\', \'valid\', 1, \'Factorizationnumcores\', \'4\', 1, \'Factorizationtimesec\', \'0.557165\', 1, \'Factorizationmentotalkb\', \'487542.000000\')', false, true)
					ProfileItem('fbsinfo', 0, 0, 0, 0, 0, 'I(10, 1, \'Fbstatus\', \'valid\', 1, \'Fbstype\', \'fullsolve\', 1, \'Fbsmt\', \'false\', 1, \'Fbsmrhs\', \'false\', 1, \'Fbsnumcores\', \'4\', 1, \'Fbsnumsolvestotal\', \'8\', 1, \'Fbsnumsolves\', \'5\', 1, \'Fbsavgsolvetime1solvesec\', \'0.041025\', 1, \'Fbscputimesec\', \'0.205125\', 1, \'Fbsmemorytotalkb\', \'420432.000000\')', false, true)
					ProfileItem('solverprofile', 0, 0, 0, 0, 0, 'I(2, 1, \'Maxmemkb\', \'780652\', 1, \'Maxdiskkb\', \'0\')', false, true)
				$end 'ProfileGroup'
				ProfileFootnote('I(1, 3, \'Max Mag. Delta S\', 0.718308, \'%.5f\')', 0)
			$end 'ProfileGroup'
			ProfileItem('', 0, 0, 0, 0, 0, 'I(1, 0, \'\')', false, true)
			$begin 'ProfileGroup'
				MajorVer=2025
				MinorVer=2
				Name='Adaptive Pass 3'
				$begin 'StartInfo'
					I(1, 'Frequency', '56GHz')
				$end 'StartInfo'
				$begin 'TotalInfo'
					I(0, ' ')
				$end 'TotalInfo'
				GroupOptions=0
				TaskDataOptions('CPU Time'=8, Memory=8, 'Real Time'=8)
				ProfileItem('Adaptive Refine', 0, 0, 0, 0, 65952, 'I(1, 2, \'Tetrahedra\', 37485, false)', true, true)
				ProfileItem(' ', 0, 0, 0, 0, 0, 'I(1, 0, \'\')', false, true)
				ProfileItem('Simulation Setup ', 0, 0, 0, 0, 262048, 'I(2, 2, \'Tetrahedra\', 25355, false, 1, \'Disk\', \'15.4 KB\')', true, true)
				ProfileItem('Matrix Assembly', 1, 0, 3, 0, 491060, 'I(4, 2, \'Tetrahedra\', 25355, false, 2, \'Lumped ports\', 2, false, 2, \'P1 Triangles\', 79, false, 1, \'Disk\', \'446 Bytes\')', true, true)
				ProfileItem('Matrix Solve', 1, 0, 6, 0, 978060, 'I(5, 1, \'Type\', \'DCS\', 2, \'Cores\', 4, false, 2, \'Matrix size\', 164532, false, 3, \'Matrix bandwidth\', 20.0833, \'%5.1f\', 1, \'Disk\', \'644 KB\')', true, true)
				ProfileItem('Field Recovery', 0, 0, 2, 0, 978060, 'I(3, 2, \'Excitations\', 4, false, 3, \'Average order\', 0.945879, \'%f\', 1, \'Disk\', \'1.45 MB\')', true, true)
				ProfileItem('Data Transfer', 0, 0, 0, 0, 98344, 'I(1, 0, \'Adaptive Pass 3\')', true, true)
				$begin 'ProfileGroup'
					MajorVer=2025
					MinorVer=2
					Name='APIPms'
					$begin 'StartInfo'
						I(1, 'Timesinceepock', '1754552492')
					$end 'StartInfo'
					$begin 'TotalInfo'
						I(0, ' ')
					$end 'TotalInfo'
					GroupOptions=16
					TaskDataOptions(Memory=8)
					ProfileItem('solverinfo', 0, 0, 0, 0, 0, 'I(10, 1, \'Solvertype\', \'shared_memory\', 1, \'Precision\', \'double\', 1, \'Solversymmetry\', \'complex_sym\', 1, \'Matrixdim\', \'164532\', 1, \'Matrixbw\', \'20.108900\', 1, \'Matrixnnz\', \'3308557\', 1, \'Rootdim\', \'525\', 1, \'Mathtype\', \'amd\', 1, \'Mpitasks\', \'1\', 1, \'Threadspertasks\', \'0\')', false, true)
					ProfileItem('sysinfo', 0, 0, 0, 0, 0, 'I(12, 1, \'Os\', \'win\', 1, \'Cpuid\', \'AMD Ryzen 9 8945HS w/ Radeon 780M Graphics\', 1, \'CpuPhysicCores\', \'8\', 1, \'CpuLogicCores\', \'16\', 1, \'Cpufreqkhz\', \'26601699328.000000\', 1, \'Cpucachelinesizebytes\', \'64\', 1, \'Cpuestlastlevelcachesizemb\', \'64.000000\', 1, \'Cpuestgflops\', \'524.799988\', 1, \'Memorybwestkbps\', \'51.200001\', 1, \'Numanodes\', \'1\', 1, \'Virtualmemkb\', \'137439000000.000000\', 1, \'Pagesizekb\', \'4096\')', false, true)
					ProfileItem('analysisinfo', 0, 0, 0, 0, 0, 'I(9, 1, \'Analysisstatus\', \'valid\', 1, \'Numsupernodes\', \'14693\', 1, \'Factornnz\', \'31980671\', 1, \'Factorestflops\', \'32835400000\', 1, \'Fbsestflops\', \'106075396\', 1, \'Rootfactestflops\', \'48237176\', 1, \'Rootfbsestflops\', \'137812\', 1, \'Analysistimesec\', \'0.707394\', 1, \'Analysismemkb\', \'94100.000000\')', false, true)
					ProfileItem('factorinfo', 0, 0, 0, 0, 0, 'I(4, 1, \'Fatorizationstatus\', \'valid\', 1, \'Factorizationnumcores\', \'4\', 1, \'Factorizationtimesec\', \'0.842301\', 1, \'Factorizationmentotalkb\', \'671015.000000\')', false, true)
					ProfileItem('fbsinfo', 0, 0, 0, 0, 0, 'I(10, 1, \'Fbstatus\', \'valid\', 1, \'Fbstype\', \'fullsolve\', 1, \'Fbsmt\', \'false\', 1, \'Fbsmrhs\', \'false\', 1, \'Fbsnumcores\', \'4\', 1, \'Fbsnumsolvestotal\', \'8\', 1, \'Fbsnumsolves\', \'5\', 1, \'Fbsavgsolvetime1solvesec\', \'0.058586\', 1, \'Fbscputimesec\', \'0.292933\', 1, \'Fbsmemorytotalkb\', \'572716.000000\')', false, true)
					ProfileItem('solverprofile', 0, 0, 0, 0, 0, 'I(2, 1, \'Maxmemkb\', \'978060\', 1, \'Maxdiskkb\', \'0\')', false, true)
				$end 'ProfileGroup'
				ProfileFootnote('I(1, 3, \'Max Mag. Delta S\', 0.215759, \'%.5f\')', 0)
			$end 'ProfileGroup'
			ProfileItem('', 0, 0, 0, 0, 0, 'I(1, 0, \'\')', false, true)
			$begin 'ProfileGroup'
				MajorVer=2025
				MinorVer=2
				Name='Adaptive Pass 4'
				$begin 'StartInfo'
					I(1, 'Frequency', '56GHz')
				$end 'StartInfo'
				$begin 'TotalInfo'
					I(0, ' ')
				$end 'TotalInfo'
				GroupOptions=0
				TaskDataOptions('CPU Time'=8, Memory=8, 'Real Time'=8)
				ProfileItem('Adaptive Refine', 1, 0, 1, 0, 72996, 'I(1, 2, \'Tetrahedra\', 44932, false)', true, true)
				ProfileItem(' ', 0, 0, 0, 0, 0, 'I(1, 0, \'\')', false, true)
				ProfileItem('Simulation Setup ', 0, 0, 0, 0, 279532, 'I(2, 2, \'Tetrahedra\', 32202, false, 1, \'Disk\', \'20.5 KB\')', true, true)
				ProfileItem('Matrix Assembly', 1, 0, 3, 0, 571144, 'I(4, 2, \'Tetrahedra\', 32202, false, 2, \'Lumped ports\', 2, false, 2, \'P1 Triangles\', 88, false, 1, \'Disk\', \'736 Bytes\')', true, true)
				ProfileItem('Matrix Solve', 2, 0, 8, 0, 1294748, 'I(5, 1, \'Type\', \'DCS\', 2, \'Cores\', 4, false, 2, \'Matrix size\', 208934, false, 3, \'Matrix bandwidth\', 20.4273, \'%5.1f\', 1, \'Disk\', \'818 KB\')', true, true)
				ProfileItem('Field Recovery', 0, 0, 3, 0, 1294748, 'I(3, 2, \'Excitations\', 4, false, 3, \'Average order\', 0.95779, \'%f\', 1, \'Disk\', \'1.76 MB\')', true, true)
				ProfileItem('Data Transfer', 0, 0, 0, 0, 98348, 'I(1, 0, \'Adaptive Pass 4\')', true, true)
				$begin 'ProfileGroup'
					MajorVer=2025
					MinorVer=2
					Name='APIPms'
					$begin 'StartInfo'
						I(1, 'Timesinceepock', '1754552502')
					$end 'StartInfo'
					$begin 'TotalInfo'
						I(0, ' ')
					$end 'TotalInfo'
					GroupOptions=16
					TaskDataOptions(Memory=8)
					ProfileItem('solverinfo', 0, 0, 0, 0, 0, 'I(10, 1, \'Solvertype\', \'shared_memory\', 1, \'Precision\', \'double\', 1, \'Solversymmetry\', \'complex_sym\', 1, \'Matrixdim\', \'208934\', 1, \'Matrixbw\', \'20.451300\', 1, \'Matrixnnz\', \'4272972\', 1, \'Rootdim\', \'659\', 1, \'Mathtype\', \'amd\', 1, \'Mpitasks\', \'1\', 1, \'Threadspertasks\', \'0\')', false, true)
					ProfileItem('sysinfo', 0, 0, 0, 0, 0, 'I(12, 1, \'Os\', \'win\', 1, \'Cpuid\', \'AMD Ryzen 9 8945HS w/ Radeon 780M Graphics\', 1, \'CpuPhysicCores\', \'8\', 1, \'CpuLogicCores\', \'16\', 1, \'Cpufreqkhz\', \'26546499584.000000\', 1, \'Cpucachelinesizebytes\', \'64\', 1, \'Cpuestlastlevelcachesizemb\', \'64.000000\', 1, \'Cpuestgflops\', \'524.799988\', 1, \'Memorybwestkbps\', \'51.200001\', 1, \'Numanodes\', \'1\', 1, \'Virtualmemkb\', \'137439000000.000000\', 1, \'Pagesizekb\', \'4096\')', false, true)
					ProfileItem('analysisinfo', 0, 0, 0, 0, 0, 'I(9, 1, \'Analysisstatus\', \'valid\', 1, \'Numsupernodes\', \'18565\', 1, \'Factornnz\', \'46811142\', 1, \'Factorestflops\', \'58925200000\', 1, \'Fbsestflops\', \'157456221\', 1, \'Rootfactestflops\', \'95400850\', 1, \'Rootfbsestflops\', \'217140\', 1, \'Analysistimesec\', \'0.990309\', 1, \'Analysismemkb\', \'121736.000000\')', false, true)
					ProfileItem('factorinfo', 0, 0, 0, 0, 0, 'I(4, 1, \'Fatorizationstatus\', \'valid\', 1, \'Factorizationnumcores\', \'4\', 1, \'Factorizationtimesec\', \'1.304530\', 1, \'Factorizationmentotalkb\', \'972350.000000\')', false, true)
					ProfileItem('fbsinfo', 0, 0, 0, 0, 0, 'I(10, 1, \'Fbstatus\', \'valid\', 1, \'Fbstype\', \'fullsolve\', 1, \'Fbsmt\', \'false\', 1, \'Fbsmrhs\', \'false\', 1, \'Fbsnumcores\', \'4\', 1, \'Fbsnumsolvestotal\', \'8\', 1, \'Fbsnumsolves\', \'5\', 1, \'Fbsavgsolvetime1solvesec\', \'0.074515\', 1, \'Fbscputimesec\', \'0.372577\', 1, \'Fbsmemorytotalkb\', \'834268.000000\')', false, true)
					ProfileItem('solverprofile', 0, 0, 0, 0, 0, 'I(2, 1, \'Maxmemkb\', \'1294748\', 1, \'Maxdiskkb\', \'0\')', false, true)
				$end 'ProfileGroup'
				ProfileFootnote('I(1, 3, \'Max Mag. Delta S\', 0.0641126, \'%.5f\')', 0)
			$end 'ProfileGroup'
			ProfileItem('', 0, 0, 0, 0, 0, 'I(1, 0, \'\')', false, true)
			$begin 'ProfileGroup'
				MajorVer=2025
				MinorVer=2
				Name='Adaptive Pass 5'
				$begin 'StartInfo'
					I(1, 'Frequency', '56GHz')
				$end 'StartInfo'
				$begin 'TotalInfo'
					I(0, ' ')
				$end 'TotalInfo'
				GroupOptions=0
				TaskDataOptions('CPU Time'=8, Memory=8, 'Real Time'=8)
				ProfileItem('Adaptive Refine', 1, 0, 1, 0, 82624, 'I(1, 2, \'Tetrahedra\', 54450, false)', true, true)
				ProfileItem(' ', 0, 0, 0, 0, 0, 'I(1, 0, \'\')', false, true)
				ProfileItem('Simulation Setup ', 0, 0, 0, 0, 300112, 'I(2, 2, \'Tetrahedra\', 41116, false, 1, \'Disk\', \'25.4 KB\')', true, true)
				ProfileItem('Matrix Assembly', 2, 0, 4, 0, 677448, 'I(4, 2, \'Tetrahedra\', 41116, false, 2, \'Lumped ports\', 2, false, 2, \'P1 Triangles\', 102, false, 1, \'Disk\', \'1.17 KB\')', true, true)
				ProfileItem('Matrix Solve', 3, 0, 11, 0, 1686432, 'I(5, 1, \'Type\', \'DCS\', 2, \'Cores\', 4, false, 2, \'Matrix size\', 266439, false, 3, \'Matrix bandwidth\', 20.7302, \'%5.1f\', 1, \'Disk\', \'1.02 MB\')', true, true)
				ProfileItem('Field Recovery', 1, 0, 4, 0, 1686432, 'I(3, 2, \'Excitations\', 4, false, 3, \'Average order\', 0.967087, \'%f\', 1, \'Disk\', \'2.15 MB\')', true, true)
				ProfileItem('Data Transfer', 0, 0, 0, 0, 98324, 'I(1, 0, \'Adaptive Pass 5\')', true, true)
				$begin 'ProfileGroup'
					MajorVer=2025
					MinorVer=2
					Name='APIPms'
					$begin 'StartInfo'
						I(1, 'Timesinceepock', '1754552512')
					$end 'StartInfo'
					$begin 'TotalInfo'
						I(0, ' ')
					$end 'TotalInfo'
					GroupOptions=16
					TaskDataOptions(Memory=8)
					ProfileItem('solverinfo', 0, 0, 0, 0, 0, 'I(10, 1, \'Solvertype\', \'shared_memory\', 1, \'Precision\', \'double\', 1, \'Solversymmetry\', \'complex_sym\', 1, \'Matrixdim\', \'266439\', 1, \'Matrixbw\', \'20.752300\', 1, \'Matrixnnz\', \'5529226\', 1, \'Rootdim\', \'876\', 1, \'Mathtype\', \'amd\', 1, \'Mpitasks\', \'1\', 1, \'Threadspertasks\', \'0\')', false, true)
					ProfileItem('sysinfo', 0, 0, 0, 0, 0, 'I(12, 1, \'Os\', \'win\', 1, \'Cpuid\', \'AMD Ryzen 9 8945HS w/ Radeon 780M Graphics\', 1, \'CpuPhysicCores\', \'8\', 1, \'CpuLogicCores\', \'16\', 1, \'Cpufreqkhz\', \'26474700800.000000\', 1, \'Cpucachelinesizebytes\', \'64\', 1, \'Cpuestlastlevelcachesizemb\', \'64.000000\', 1, \'Cpuestgflops\', \'524.799988\', 1, \'Memorybwestkbps\', \'51.200001\', 1, \'Numanodes\', \'1\', 1, \'Virtualmemkb\', \'137439000000.000000\', 1, \'Pagesizekb\', \'4096\')', false, true)
					ProfileItem('analysisinfo', 0, 0, 0, 0, 0, 'I(9, 1, \'Analysisstatus\', \'valid\', 1, \'Numsupernodes\', \'23715\', 1, \'Factornnz\', \'65149814\', 1, \'Factorestflops\', \'90351100000\', 1, \'Fbsestflops\', \'220661271\', 1, \'Rootfactestflops\', \'224078563\', 1, \'Rootfbsestflops\', \'383688\', 1, \'Analysistimesec\', \'1.369120\', 1, \'Analysismemkb\', \'158100.000000\')', false, true)
					ProfileItem('factorinfo', 0, 0, 0, 0, 0, 'I(4, 1, \'Fatorizationstatus\', \'valid\', 1, \'Factorizationnumcores\', \'4\', 1, \'Factorizationtimesec\', \'1.942920\', 1, \'Factorizationmentotalkb\', \'1315070.000000\')', false, true)
					ProfileItem('fbsinfo', 0, 0, 0, 0, 0, 'I(10, 1, \'Fbstatus\', \'valid\', 1, \'Fbstype\', \'fullsolve\', 1, \'Fbsmt\', \'false\', 1, \'Fbsmrhs\', \'false\', 1, \'Fbsnumcores\', \'4\', 1, \'Fbsnumsolvestotal\', \'8\', 1, \'Fbsnumsolves\', \'5\', 1, \'Fbsavgsolvetime1solvesec\', \'0.118203\', 1, \'Fbscputimesec\', \'0.591017\', 1, \'Fbsmemorytotalkb\', \'1155200.000000\')', false, true)
					ProfileItem('solverprofile', 0, 0, 0, 0, 0, 'I(2, 1, \'Maxmemkb\', \'1686432\', 1, \'Maxdiskkb\', \'0\')', false, true)
				$end 'ProfileGroup'
				ProfileFootnote('I(1, 3, \'Max Mag. Delta S\', 0.0451103, \'%.5f\')', 0)
			$end 'ProfileGroup'
			ProfileItem('', 0, 0, 0, 0, 0, 'I(1, 0, \'\')', false, true)
			$begin 'ProfileGroup'
				MajorVer=2025
				MinorVer=2
				Name='Adaptive Pass 6'
				$begin 'StartInfo'
					I(1, 'Frequency', '56GHz')
				$end 'StartInfo'
				$begin 'TotalInfo'
					I(0, ' ')
				$end 'TotalInfo'
				GroupOptions=0
				TaskDataOptions('CPU Time'=8, Memory=8, 'Real Time'=8)
				ProfileItem('Adaptive Refine', 1, 0, 1, 0, 97568, 'I(1, 2, \'Tetrahedra\', 66701, false)', true, true)
				ProfileItem(' ', 0, 0, 0, 0, 0, 'I(1, 0, \'\')', false, true)
				ProfileItem('Simulation Setup ', 0, 0, 0, 0, 328124, 'I(2, 2, \'Tetrahedra\', 52658, false, 1, \'Disk\', \'34.8 KB\')', true, true)
				ProfileItem('Matrix Assembly', 2, 0, 5, 0, 811820, 'I(4, 2, \'Tetrahedra\', 52658, false, 2, \'Lumped ports\', 2, false, 2, \'P1 Triangles\', 119, false, 1, \'Disk\', \'1.62 KB\')', true, true)
				ProfileItem('Matrix Solve', 5, 0, 16, 0, 2203944, 'I(5, 1, \'Type\', \'DCS\', 2, \'Cores\', 4, false, 2, \'Matrix size\', 340572, false, 3, \'Matrix bandwidth\', 20.9767, \'%5.1f\', 1, \'Disk\', \'1.3 MB\')', true, true)
				ProfileItem('Field Recovery', 1, 0, 5, 0, 2203944, 'I(3, 2, \'Excitations\', 4, false, 3, \'Average order\', 0.974363, \'%f\', 1, \'Disk\', \'2.65 MB\')', true, true)
				ProfileItem('Data Transfer', 0, 0, 0, 0, 98316, 'I(1, 0, \'Adaptive Pass 6\')', true, true)
				$begin 'ProfileGroup'
					MajorVer=2025
					MinorVer=2
					Name='APIPms'
					$begin 'StartInfo'
						I(1, 'Timesinceepock', '1754552525')
					$end 'StartInfo'
					$begin 'TotalInfo'
						I(0, ' ')
					$end 'TotalInfo'
					GroupOptions=16
					TaskDataOptions(Memory=8)
					ProfileItem('solverinfo', 0, 0, 0, 0, 0, 'I(10, 1, \'Solvertype\', \'shared_memory\', 1, \'Precision\', \'double\', 1, \'Solversymmetry\', \'complex_sym\', 1, \'Matrixdim\', \'340572\', 1, \'Matrixbw\', \'20.997700\', 1, \'Matrixnnz\', \'7151244\', 1, \'Rootdim\', \'1125\', 1, \'Mathtype\', \'amd\', 1, \'Mpitasks\', \'1\', 1, \'Threadspertasks\', \'0\')', false, true)
					ProfileItem('sysinfo', 0, 0, 0, 0, 0, 'I(12, 1, \'Os\', \'win\', 1, \'Cpuid\', \'AMD Ryzen 9 8945HS w/ Radeon 780M Graphics\', 1, \'CpuPhysicCores\', \'8\', 1, \'CpuLogicCores\', \'16\', 1, \'Cpufreqkhz\', \'26379200512.000000\', 1, \'Cpucachelinesizebytes\', \'64\', 1, \'Cpuestlastlevelcachesizemb\', \'64.000000\', 1, \'Cpuestgflops\', \'524.799988\', 1, \'Memorybwestkbps\', \'51.200001\', 1, \'Numanodes\', \'1\', 1, \'Virtualmemkb\', \'137439000000.000000\', 1, \'Pagesizekb\', \'4096\')', false, true)
					ProfileItem('analysisinfo', 0, 0, 0, 0, 0, 'I(9, 1, \'Analysisstatus\', \'valid\', 1, \'Numsupernodes\', \'30082\', 1, \'Factornnz\', \'90304591\', 1, \'Factorestflops\', \'139601000000\', 1, \'Fbsestflops\', \'308965623\', 1, \'Rootfactestflops\', \'474615265\', 1, \'Rootfbsestflops\', \'632812\', 1, \'Analysistimesec\', \'1.804620\', 1, \'Analysismemkb\', \'204852.000000\')', false, true)
					ProfileItem('factorinfo', 0, 0, 0, 0, 0, 'I(4, 1, \'Fatorizationstatus\', \'valid\', 1, \'Factorizationnumcores\', \'4\', 1, \'Factorizationtimesec\', \'2.945050\', 1, \'Factorizationmentotalkb\', \'1807220.000000\')', false, true)
					ProfileItem('fbsinfo', 0, 0, 0, 0, 0, 'I(10, 1, \'Fbstatus\', \'valid\', 1, \'Fbstype\', \'fullsolve\', 1, \'Fbsmt\', \'false\', 1, \'Fbsmrhs\', \'false\', 1, \'Fbsnumcores\', \'4\', 1, \'Fbsnumsolvestotal\', \'8\', 1, \'Fbsnumsolves\', \'5\', 1, \'Fbsavgsolvetime1solvesec\', \'0.185954\', 1, \'Fbscputimesec\', \'0.929771\', 1, \'Fbsmemorytotalkb\', \'1578500.000000\')', false, true)
					ProfileItem('solverprofile', 0, 0, 0, 0, 0, 'I(2, 1, \'Maxmemkb\', \'2203944\', 1, \'Maxdiskkb\', \'0\')', false, true)
				$end 'ProfileGroup'
				ProfileFootnote('I(1, 3, \'Max Mag. Delta S\', 0.0233549, \'%.5f\')', 0)
			$end 'ProfileGroup'
			ProfileItem('', 0, 0, 0, 0, 0, 'I(1, 0, \'\')', false, true)
			$begin 'ProfileGroup'
				MajorVer=2025
				MinorVer=2
				Name='Adaptive Pass 7'
				$begin 'StartInfo'
					I(1, 'Frequency', '56GHz')
				$end 'StartInfo'
				$begin 'TotalInfo'
					I(0, ' ')
				$end 'TotalInfo'
				GroupOptions=0
				TaskDataOptions('CPU Time'=8, Memory=8, 'Real Time'=8)
				ProfileItem('Adaptive Refine', 2, 0, 2, 0, 115344, 'I(1, 2, \'Tetrahedra\', 82416, false)', true, true)
				ProfileItem(' ', 0, 0, 0, 0, 0, 'I(1, 0, \'\')', false, true)
				ProfileItem('Simulation Setup ', 1, 0, 1, 0, 360444, 'I(2, 2, \'Tetrahedra\', 67502, false, 1, \'Disk\', \'39.8 KB\')', true, true)
				ProfileItem('Matrix Assembly', 3, 0, 7, 0, 982680, 'I(4, 2, \'Tetrahedra\', 67502, false, 2, \'Lumped ports\', 2, false, 2, \'P1 Triangles\', 130, false, 1, \'Disk\', \'1.84 KB\')', true, true)
				ProfileItem('Matrix Solve', 6, 0, 22, 0, 2885956, 'I(5, 1, \'Type\', \'DCS\', 2, \'Cores\', 4, false, 2, \'Matrix size\', 435862, false, 3, \'Matrix bandwidth\', 21.1632, \'%5.1f\', 1, \'Disk\', \'1.66 MB\')', true, true)
				ProfileItem('Field Recovery', 1, 0, 6, 0, 2885956, 'I(3, 2, \'Excitations\', 4, false, 3, \'Average order\', 0.980049, \'%f\', 1, \'Disk\', \'3.29 MB\')', true, true)
				ProfileItem('Data Transfer', 0, 0, 0, 0, 98316, 'I(1, 0, \'Adaptive Pass 7\')', true, true)
				$begin 'ProfileGroup'
					MajorVer=2025
					MinorVer=2
					Name='APIPms'
					$begin 'StartInfo'
						I(1, 'Timesinceepock', '1754552544')
					$end 'StartInfo'
					$begin 'TotalInfo'
						I(0, ' ')
					$end 'TotalInfo'
					GroupOptions=16
					TaskDataOptions(Memory=8)
					ProfileItem('solverinfo', 0, 0, 0, 0, 0, 'I(10, 1, \'Solvertype\', \'shared_memory\', 1, \'Precision\', \'double\', 1, \'Solversymmetry\', \'complex_sym\', 1, \'Matrixdim\', \'435862\', 1, \'Matrixbw\', \'21.183500\', 1, \'Matrixnnz\', \'9233090\', 1, \'Rootdim\', \'1121\', 1, \'Mathtype\', \'amd\', 1, \'Mpitasks\', \'1\', 1, \'Threadspertasks\', \'0\')', false, true)
					ProfileItem('sysinfo', 0, 0, 0, 0, 0, 'I(12, 1, \'Os\', \'win\', 1, \'Cpuid\', \'AMD Ryzen 9 8945HS w/ Radeon 780M Graphics\', 1, \'CpuPhysicCores\', \'8\', 1, \'CpuLogicCores\', \'16\', 1, \'Cpufreqkhz\', \'26262900736.000000\', 1, \'Cpucachelinesizebytes\', \'64\', 1, \'Cpuestlastlevelcachesizemb\', \'64.000000\', 1, \'Cpuestgflops\', \'524.799988\', 1, \'Memorybwestkbps\', \'51.200001\', 1, \'Numanodes\', \'1\', 1, \'Virtualmemkb\', \'137439000000.000000\', 1, \'Pagesizekb\', \'4096\')', false, true)
					ProfileItem('analysisinfo', 0, 0, 0, 0, 0, 'I(9, 1, \'Analysisstatus\', \'valid\', 1, \'Numsupernodes\', \'38288\', 1, \'Factornnz\', \'123710117\', 1, \'Factorestflops\', \'210992000000\', 1, \'Fbsestflops\', \'419882545\', 1, \'Rootfactestflops\', \'469570897\', 1, \'Rootfbsestflops\', \'628320\', 1, \'Analysistimesec\', \'2.415610\', 1, \'Analysismemkb\', \'264876.000000\')', false, true)
					ProfileItem('factorinfo', 0, 0, 0, 0, 0, 'I(4, 1, \'Fatorizationstatus\', \'valid\', 1, \'Factorizationnumcores\', \'4\', 1, \'Factorizationtimesec\', \'3.922560\', 1, \'Factorizationmentotalkb\', \'2447630.000000\')', false, true)
					ProfileItem('fbsinfo', 0, 0, 0, 0, 0, 'I(10, 1, \'Fbstatus\', \'valid\', 1, \'Fbstype\', \'fullsolve\', 1, \'Fbsmt\', \'false\', 1, \'Fbsmrhs\', \'false\', 1, \'Fbsnumcores\', \'4\', 1, \'Fbsnumsolvestotal\', \'8\', 1, \'Fbsnumsolves\', \'5\', 1, \'Fbsavgsolvetime1solvesec\', \'0.200337\', 1, \'Fbscputimesec\', \'1.001690\', 1, \'Fbsmemorytotalkb\', \'2144250.000000\')', false, true)
					ProfileItem('solverprofile', 0, 0, 0, 0, 0, 'I(2, 1, \'Maxmemkb\', \'2885956\', 1, \'Maxdiskkb\', \'0\')', false, true)
				$end 'ProfileGroup'
				ProfileFootnote('I(1, 3, \'Max Mag. Delta S\', 0.0160731, \'%.5f\')', 0)
			$end 'ProfileGroup'
			ProfileFootnote('I(1, 0, \'Adaptive Passes converged\')', 0)
		$end 'ProfileGroup'
		ProfileItem('', 0, 0, 0, 0, 0, 'I(1, 0, \'\')', false, true)
		$begin 'ProfileGroup'
			MajorVer=2025
			MinorVer=2
			Name='Simulation Summary'
			$begin 'StartInfo'
			$end 'StartInfo'
			$begin 'TotalInfo'
				I(0, ' ')
			$end 'TotalInfo'
			GroupOptions=0
			TaskDataOptions('CPU Time'=8, Memory=8, 'Real Time'=8)
			ProfileItem('Design Validation', 0, 0, 0, 0, 0, 'I(2, 1, \'Elapsed Time\', \'00:00:00\', 1, \'Total Memory\', \'89.2 MB\')', false, true)
			ProfileItem('Initial Meshing', 0, 0, 0, 0, 0, 'I(2, 1, \'Elapsed Time\', \'00:00:23\', 1, \'Total Memory\', \'372 MB\')', false, true)
			ProfileItem('Adaptive Meshing', 0, 0, 0, 0, 0, 'I(5, 1, \'Elapsed Time\', \'00:01:11\', 1, \'Average memory/process\', \'2.75 GB\', 1, \'Max memory/process\', \'2.75 GB\', 2, \'Max number of processes/frequency\', 1, false, 2, \'Total number of cores\', 4, false)', false, true)
			ProfileFootnote('I(3, 2, \'Max solved tets\', 67502, false, 2, \'Max matrix size\', 435862, false, 1, \'Matrix bandwidth\', \'21.2\')', 0)
		$end 'ProfileGroup'
		ProfileFootnote('I(2, 1, \'Stop Time\', \'08/07/2025 15:42:27\', 1, \'Status\', \'Normal Completion\')', 0)
	$end 'ProfileGroup'
$end 'Profile'
