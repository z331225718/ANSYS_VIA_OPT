$begin 'Profile'
	$begin 'ProfileGroup'
		MajorVer=2025
		MinorVer=2
		Name='Solution Process'
		$begin 'StartInfo'
			I(1, 'Start Time', '08/07/2025 15:36:12')
			I(1, 'Host', 'ZZMJAY')
			I(1, 'Processor', '16')
			I(1, 'OS', 'NT 10.0')
			I(1, 'Product', 'HFSS Version 2025.2.0')
		$end 'StartInfo'
		$begin 'TotalInfo'
			I(1, 'Elapsed Time', '00:01:32')
			I(1, 'ComEngine Memory', '95.5 M')
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
		ProfileItem('Design Validation', 0, 0, 0, 0, 0, 'I(1, 0, \'Elapsed time : 00:00:00 , HFSS ComEngine Memory : 89.1 M\')', false, true)
		ProfileItem('', 0, 0, 0, 0, 0, 'I(1, 0, \'Perform full validations with standard port validations\')', false, true)
		ProfileItem('', 0, 0, 0, 0, 0, 'I(1, 0, \'\')', false, true)
		$begin 'ProfileGroup'
			MajorVer=2025
			MinorVer=2
			Name='Initial Meshing'
			$begin 'StartInfo'
				I(1, 'Time', '08/07/2025 15:36:12')
			$end 'StartInfo'
			$begin 'TotalInfo'
				I(1, 'Elapsed Time', '00:00:22')
			$end 'TotalInfo'
			GroupOptions=4
			TaskDataOptions('CPU Time'=8, Memory=8, 'Real Time'=8)
			ProfileItem('Mesh', 17, 0, 21, 0, 137000, 'I(3, 2, \'Tetrahedra\', 62643, false, 1, \'Type\', \'TAU\', 2, \'Cores\', 4, false)', true, true)
			ProfileItem('Coarsen', 1, 0, 1, 0, 137000, 'I(1, 2, \'Tetrahedra\', 26196, false)', true, true)
			ProfileItem('Lambda Refine', 0, 0, 0, 0, 46892, 'I(1, 2, \'Tetrahedra\', 26790, false)', true, true)
			ProfileItem('Simulation Setup', 0, 0, 0, 0, 231316, 'I(2, 2, \'Tetrahedra\', 15511, false, 1, \'Disk\', \'0 Bytes\')', true, true)
			ProfileItem('Port Adapt', 0, 0, 0, 0, 243836, 'I(2, 2, \'Tetrahedra\', 15511, false, 1, \'Disk\', \'12 KB\')', true, true)
			ProfileItem('Port Refine', 0, 0, 0, 0, 53656, 'I(1, 2, \'Tetrahedra\', 26909, false)', true, true)
		$end 'ProfileGroup'
		$begin 'ProfileGroup'
			MajorVer=2025
			MinorVer=2
			Name='Adaptive Meshing'
			$begin 'StartInfo'
				I(1, 'Time', '08/07/2025 15:36:34')
			$end 'StartInfo'
			$begin 'TotalInfo'
				I(1, 'Elapsed Time', '00:01:09')
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
				ProfileItem('Simulation Setup ', 0, 0, 0, 0, 238140, 'I(2, 2, \'Tetrahedra\', 15680, false, 1, \'Disk\', \'10.5 KB\')', true, true)
				ProfileItem('Matrix Assembly', 1, 0, 1, 0, 371236, 'I(4, 2, \'Tetrahedra\', 15680, false, 2, \'Lumped ports\', 2, false, 2, \'P1 Triangles\', 87, false, 1, \'Disk\', \'135 KB\')', true, true)
				ProfileItem('Matrix Solve', 0, 0, 3, 0, 580564, 'I(5, 1, \'Type\', \'DCS\', 2, \'Cores\', 4, false, 2, \'Matrix size\', 99108, false, 3, \'Matrix bandwidth\', 19.1509, \'%5.1f\', 1, \'Disk\', \'390 KB\')', true, true)
				ProfileItem('Field Recovery', 0, 0, 1, 0, 580564, 'I(3, 2, \'Excitations\', 4, false, 3, \'Average order\', 0.888042, \'%f\', 1, \'Disk\', \'2.36 MB\')', true, true)
				ProfileItem('Data Transfer', 0, 0, 0, 0, 95708, 'I(1, 0, \'Adaptive Pass 1\')', true, true)
				$begin 'ProfileGroup'
					MajorVer=2025
					MinorVer=2
					Name='APIPms'
					$begin 'StartInfo'
						I(1, 'Timesinceepock', '1754552198')
					$end 'StartInfo'
					$begin 'TotalInfo'
						I(0, ' ')
					$end 'TotalInfo'
					GroupOptions=16
					TaskDataOptions(Memory=8)
					ProfileItem('solverinfo', 0, 0, 0, 0, 0, 'I(10, 1, \'Solvertype\', \'shared_memory\', 1, \'Precision\', \'double\', 1, \'Solversymmetry\', \'complex_sym\', 1, \'Matrixdim\', \'99108\', 1, \'Matrixbw\', \'19.171499\', 1, \'Matrixnnz\', \'1900052\', 1, \'Rootdim\', \'272\', 1, \'Mathtype\', \'amd\', 1, \'Mpitasks\', \'1\', 1, \'Threadspertasks\', \'0\')', false, true)
					ProfileItem('sysinfo', 0, 0, 0, 0, 0, 'I(12, 1, \'Os\', \'win\', 1, \'Cpuid\', \'AMD Ryzen 9 8945HS w/ Radeon 780M Graphics\', 1, \'CpuPhysicCores\', \'8\', 1, \'CpuLogicCores\', \'16\', 1, \'Cpufreqkhz\', \'26719600640.000000\', 1, \'Cpucachelinesizebytes\', \'64\', 1, \'Cpuestlastlevelcachesizemb\', \'64.000000\', 1, \'Cpuestgflops\', \'524.799988\', 1, \'Memorybwestkbps\', \'51.200001\', 1, \'Numanodes\', \'1\', 1, \'Virtualmemkb\', \'137439000000.000000\', 1, \'Pagesizekb\', \'4096\')', false, true)
					ProfileItem('analysisinfo', 0, 0, 0, 0, 0, 'I(9, 1, \'Analysisstatus\', \'valid\', 1, \'Numsupernodes\', \'8978\', 1, \'Factornnz\', \'13684299\', 1, \'Factorestflops\', \'8649370000\', 1, \'Fbsestflops\', \'43601172\', 1, \'Rootfactestflops\', \'6709241\', 1, \'Rootfbsestflops\', \'36992\', 1, \'Analysistimesec\', \'0.351445\', 1, \'Analysismemkb\', \'53892.000000\')', false, true)
					ProfileItem('factorinfo', 0, 0, 0, 0, 0, 'I(4, 1, \'Fatorizationstatus\', \'valid\', 1, \'Factorizationnumcores\', \'4\', 1, \'Factorizationtimesec\', \'0.315793\', 1, \'Factorizationmentotalkb\', \'296128.000000\')', false, true)
					ProfileItem('fbsinfo', 0, 0, 0, 0, 0, 'I(10, 1, \'Fbstatus\', \'valid\', 1, \'Fbstype\', \'fullsolve\', 1, \'Fbsmt\', \'false\', 1, \'Fbsmrhs\', \'false\', 1, \'Fbsnumcores\', \'4\', 1, \'Fbsnumsolvestotal\', \'8\', 1, \'Fbsnumsolves\', \'5\', 1, \'Fbsavgsolvetime1solvesec\', \'0.027872\', 1, \'Fbscputimesec\', \'0.139361\', 1, \'Fbsmemorytotalkb\', \'258608.000000\')', false, true)
					ProfileItem('solverprofile', 0, 0, 0, 0, 0, 'I(2, 1, \'Maxmemkb\', \'580564\', 1, \'Maxdiskkb\', \'0\')', false, true)
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
				ProfileItem('Adaptive Refine', 0, 0, 0, 0, 62588, 'I(1, 2, \'Tetrahedra\', 31614, false)', true, true)
				ProfileItem(' ', 0, 0, 0, 0, 0, 'I(1, 0, \'\')', false, true)
				ProfileItem('Simulation Setup ', 0, 0, 0, 0, 248548, 'I(2, 2, \'Tetrahedra\', 19868, false, 1, \'Disk\', \'10.5 KB\')', true, true)
				ProfileItem('Matrix Assembly', 1, 0, 2, 0, 425208, 'I(4, 2, \'Tetrahedra\', 19868, false, 2, \'Lumped ports\', 2, false, 2, \'P1 Triangles\', 87, false, 1, \'Disk\', \'0 Bytes\')', true, true)
				ProfileItem('Matrix Solve', 1, 0, 4, 0, 776784, 'I(5, 1, \'Type\', \'DCS\', 2, \'Cores\', 4, false, 2, \'Matrix size\', 128472, false, 3, \'Matrix bandwidth\', 19.6506, \'%5.1f\', 1, \'Disk\', \'503 KB\')', true, true)
				ProfileItem('Field Recovery', 0, 0, 2, 0, 776784, 'I(3, 2, \'Excitations\', 4, false, 3, \'Average order\', 0.925005, \'%f\', 1, \'Disk\', \'1.24 MB\')', true, true)
				ProfileItem('Data Transfer', 0, 0, 0, 0, 95864, 'I(1, 0, \'Adaptive Pass 2\')', true, true)
				$begin 'ProfileGroup'
					MajorVer=2025
					MinorVer=2
					Name='APIPms'
					$begin 'StartInfo'
						I(1, 'Timesinceepock', '1754552205')
					$end 'StartInfo'
					$begin 'TotalInfo'
						I(0, ' ')
					$end 'TotalInfo'
					GroupOptions=16
					TaskDataOptions(Memory=8)
					ProfileItem('solverinfo', 0, 0, 0, 0, 0, 'I(10, 1, \'Solvertype\', \'shared_memory\', 1, \'Precision\', \'double\', 1, \'Solversymmetry\', \'complex_sym\', 1, \'Matrixdim\', \'128472\', 1, \'Matrixbw\', \'19.678900\', 1, \'Matrixnnz\', \'2528189\', 1, \'Rootdim\', \'438\', 1, \'Mathtype\', \'amd\', 1, \'Mpitasks\', \'1\', 1, \'Threadspertasks\', \'0\')', false, true)
					ProfileItem('sysinfo', 0, 0, 0, 0, 0, 'I(12, 1, \'Os\', \'win\', 1, \'Cpuid\', \'AMD Ryzen 9 8945HS w/ Radeon 780M Graphics\', 1, \'CpuPhysicCores\', \'8\', 1, \'CpuLogicCores\', \'16\', 1, \'Cpufreqkhz\', \'26679300096.000000\', 1, \'Cpucachelinesizebytes\', \'64\', 1, \'Cpuestlastlevelcachesizemb\', \'64.000000\', 1, \'Cpuestgflops\', \'524.799988\', 1, \'Memorybwestkbps\', \'51.200001\', 1, \'Numanodes\', \'1\', 1, \'Virtualmemkb\', \'137439000000.000000\', 1, \'Pagesizekb\', \'4096\')', false, true)
					ProfileItem('analysisinfo', 0, 0, 0, 0, 0, 'I(9, 1, \'Analysisstatus\', \'valid\', 1, \'Numsupernodes\', \'11525\', 1, \'Factornnz\', \'21937877\', 1, \'Factorestflops\', \'19125100000\', 1, \'Fbsestflops\', \'71964140\', 1, \'Rootfactestflops\', \'28011377\', 1, \'Rootfbsestflops\', \'95922\', 1, \'Analysistimesec\', \'0.527620\', 1, \'Analysismemkb\', \'71980.000000\')', false, true)
					ProfileItem('factorinfo', 0, 0, 0, 0, 0, 'I(4, 1, \'Fatorizationstatus\', \'valid\', 1, \'Factorizationnumcores\', \'4\', 1, \'Factorizationtimesec\', \'0.530645\', 1, \'Factorizationmentotalkb\', \'465094.000000\')', false, true)
					ProfileItem('fbsinfo', 0, 0, 0, 0, 0, 'I(10, 1, \'Fbstatus\', \'valid\', 1, \'Fbstype\', \'fullsolve\', 1, \'Fbsmt\', \'false\', 1, \'Fbsmrhs\', \'false\', 1, \'Fbsnumcores\', \'4\', 1, \'Fbsnumsolvestotal\', \'8\', 1, \'Fbsnumsolves\', \'5\', 1, \'Fbsavgsolvetime1solvesec\', \'0.043095\', 1, \'Fbscputimesec\', \'0.215474\', 1, \'Fbsmemorytotalkb\', \'416792.000000\')', false, true)
					ProfileItem('solverprofile', 0, 0, 0, 0, 0, 'I(2, 1, \'Maxmemkb\', \'776784\', 1, \'Maxdiskkb\', \'0\')', false, true)
				$end 'ProfileGroup'
				ProfileFootnote('I(1, 3, \'Max Mag. Delta S\', 0.734321, \'%.5f\')', 0)
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
				ProfileItem('Adaptive Refine', 0, 0, 0, 0, 63900, 'I(1, 2, \'Tetrahedra\', 37297, false)', true, true)
				ProfileItem(' ', 0, 0, 0, 0, 0, 'I(1, 0, \'\')', false, true)
				ProfileItem('Simulation Setup ', 0, 0, 0, 0, 262336, 'I(2, 2, \'Tetrahedra\', 24947, false, 1, \'Disk\', \'15.2 KB\')', true, true)
				ProfileItem('Matrix Assembly', 1, 0, 3, 0, 486156, 'I(4, 2, \'Tetrahedra\', 24947, false, 2, \'Lumped ports\', 2, false, 2, \'P1 Triangles\', 88, false, 1, \'Disk\', \'131 Bytes\')', true, true)
				ProfileItem('Matrix Solve', 1, 0, 6, 0, 992348, 'I(5, 1, \'Type\', \'DCS\', 2, \'Cores\', 4, false, 2, \'Matrix size\', 162009, false, 3, \'Matrix bandwidth\', 20.0532, \'%5.1f\', 1, \'Disk\', \'634 KB\')', true, true)
				ProfileItem('Field Recovery', 0, 0, 2, 0, 992348, 'I(3, 2, \'Excitations\', 4, false, 3, \'Average order\', 0.942258, \'%f\', 1, \'Disk\', \'1.44 MB\')', true, true)
				ProfileItem('Data Transfer', 0, 0, 0, 0, 97740, 'I(1, 0, \'Adaptive Pass 3\')', true, true)
				$begin 'ProfileGroup'
					MajorVer=2025
					MinorVer=2
					Name='APIPms'
					$begin 'StartInfo'
						I(1, 'Timesinceepock', '1754552212')
					$end 'StartInfo'
					$begin 'TotalInfo'
						I(0, ' ')
					$end 'TotalInfo'
					GroupOptions=16
					TaskDataOptions(Memory=8)
					ProfileItem('solverinfo', 0, 0, 0, 0, 0, 'I(10, 1, \'Solvertype\', \'shared_memory\', 1, \'Precision\', \'double\', 1, \'Solversymmetry\', \'complex_sym\', 1, \'Matrixdim\', \'162009\', 1, \'Matrixbw\', \'20.080099\', 1, \'Matrixnnz\', \'3253153\', 1, \'Rootdim\', \'541\', 1, \'Mathtype\', \'amd\', 1, \'Mpitasks\', \'1\', 1, \'Threadspertasks\', \'0\')', false, true)
					ProfileItem('sysinfo', 0, 0, 0, 0, 0, 'I(12, 1, \'Os\', \'win\', 1, \'Cpuid\', \'AMD Ryzen 9 8945HS w/ Radeon 780M Graphics\', 1, \'CpuPhysicCores\', \'8\', 1, \'CpuLogicCores\', \'16\', 1, \'Cpufreqkhz\', \'26635499520.000000\', 1, \'Cpucachelinesizebytes\', \'64\', 1, \'Cpuestlastlevelcachesizemb\', \'64.000000\', 1, \'Cpuestgflops\', \'524.799988\', 1, \'Memorybwestkbps\', \'51.200001\', 1, \'Numanodes\', \'1\', 1, \'Virtualmemkb\', \'137439000000.000000\', 1, \'Pagesizekb\', \'4096\')', false, true)
					ProfileItem('analysisinfo', 0, 0, 0, 0, 0, 'I(9, 1, \'Analysisstatus\', \'valid\', 1, \'Numsupernodes\', \'14522\', 1, \'Factornnz\', \'31983346\', 1, \'Factorestflops\', \'35038900000\', 1, \'Fbsestflops\', \'107253054\', 1, \'Rootfactestflops\', \'52783116\', 1, \'Rootfbsestflops\', \'146340\', 1, \'Analysistimesec\', \'0.719488\', 1, \'Analysismemkb\', \'92304.000000\')', false, true)
					ProfileItem('factorinfo', 0, 0, 0, 0, 0, 'I(4, 1, \'Fatorizationstatus\', \'valid\', 1, \'Factorizationnumcores\', \'4\', 1, \'Factorizationtimesec\', \'0.848501\', 1, \'Factorizationmentotalkb\', \'687855.000000\')', false, true)
					ProfileItem('fbsinfo', 0, 0, 0, 0, 0, 'I(10, 1, \'Fbstatus\', \'valid\', 1, \'Fbstype\', \'fullsolve\', 1, \'Fbsmt\', \'false\', 1, \'Fbsmrhs\', \'false\', 1, \'Fbsnumcores\', \'4\', 1, \'Fbsnumsolvestotal\', \'8\', 1, \'Fbsnumsolves\', \'5\', 1, \'Fbsavgsolvetime1solvesec\', \'0.055008\', 1, \'Fbscputimesec\', \'0.275040\', 1, \'Fbsmemorytotalkb\', \'590408.000000\')', false, true)
					ProfileItem('solverprofile', 0, 0, 0, 0, 0, 'I(2, 1, \'Maxmemkb\', \'992348\', 1, \'Maxdiskkb\', \'0\')', false, true)
				$end 'ProfileGroup'
				ProfileFootnote('I(1, 3, \'Max Mag. Delta S\', 0.240122, \'%.5f\')', 0)
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
				ProfileItem('Adaptive Refine', 0, 0, 0, 0, 71352, 'I(1, 2, \'Tetrahedra\', 44602, false)', true, true)
				ProfileItem(' ', 0, 0, 0, 0, 0, 'I(1, 0, \'\')', false, true)
				ProfileItem('Simulation Setup ', 0, 0, 0, 0, 278556, 'I(2, 2, \'Tetrahedra\', 31571, false, 1, \'Disk\', \'21.4 KB\')', true, true)
				ProfileItem('Matrix Assembly', 1, 0, 3, 0, 565660, 'I(4, 2, \'Tetrahedra\', 31571, false, 2, \'Lumped ports\', 2, false, 2, \'P1 Triangles\', 96, false, 1, \'Disk\', \'604 Bytes\')', true, true)
				ProfileItem('Matrix Solve', 2, 0, 8, 0, 1251796, 'I(5, 1, \'Type\', \'DCS\', 2, \'Cores\', 4, false, 2, \'Matrix size\', 205037, false, 3, \'Matrix bandwidth\', 20.3949, \'%5.1f\', 1, \'Disk\', \'803 KB\')', true, true)
				ProfileItem('Field Recovery', 0, 0, 3, 0, 1251796, 'I(3, 2, \'Excitations\', 4, false, 3, \'Average order\', 0.954895, \'%f\', 1, \'Disk\', \'1.72 MB\')', true, true)
				ProfileItem('Data Transfer', 0, 0, 0, 0, 97748, 'I(1, 0, \'Adaptive Pass 4\')', true, true)
				$begin 'ProfileGroup'
					MajorVer=2025
					MinorVer=2
					Name='APIPms'
					$begin 'StartInfo'
						I(1, 'Timesinceepock', '1754552221')
					$end 'StartInfo'
					$begin 'TotalInfo'
						I(0, ' ')
					$end 'TotalInfo'
					GroupOptions=16
					TaskDataOptions(Memory=8)
					ProfileItem('solverinfo', 0, 0, 0, 0, 0, 'I(10, 1, \'Solvertype\', \'shared_memory\', 1, \'Precision\', \'double\', 1, \'Solversymmetry\', \'complex_sym\', 1, \'Matrixdim\', \'205037\', 1, \'Matrixbw\', \'20.420099\', 1, \'Matrixnnz\', \'4186867\', 1, \'Rootdim\', \'764\', 1, \'Mathtype\', \'amd\', 1, \'Mpitasks\', \'1\', 1, \'Threadspertasks\', \'0\')', false, true)
					ProfileItem('sysinfo', 0, 0, 0, 0, 0, 'I(12, 1, \'Os\', \'win\', 1, \'Cpuid\', \'AMD Ryzen 9 8945HS w/ Radeon 780M Graphics\', 1, \'CpuPhysicCores\', \'8\', 1, \'CpuLogicCores\', \'16\', 1, \'Cpufreqkhz\', \'26580400128.000000\', 1, \'Cpucachelinesizebytes\', \'64\', 1, \'Cpuestlastlevelcachesizemb\', \'64.000000\', 1, \'Cpuestgflops\', \'524.799988\', 1, \'Memorybwestkbps\', \'51.200001\', 1, \'Numanodes\', \'1\', 1, \'Virtualmemkb\', \'137439000000.000000\', 1, \'Pagesizekb\', \'4096\')', false, true)
					ProfileItem('analysisinfo', 0, 0, 0, 0, 0, 'I(9, 1, \'Analysisstatus\', \'valid\', 1, \'Numsupernodes\', \'18259\', 1, \'Factornnz\', \'44750767\', 1, \'Factorestflops\', \'53843400000\', 1, \'Fbsestflops\', \'149987693\', 1, \'Rootfactestflops\', \'148652145\', 1, \'Rootfbsestflops\', \'291848\', 1, \'Analysistimesec\', \'0.878891\', 1, \'Analysismemkb\', \'119300.000000\')', false, true)
					ProfileItem('factorinfo', 0, 0, 0, 0, 0, 'I(4, 1, \'Fatorizationstatus\', \'valid\', 1, \'Factorizationnumcores\', \'4\', 1, \'Factorizationtimesec\', \'1.210630\', 1, \'Factorizationmentotalkb\', \'926882.000000\')', false, true)
					ProfileItem('fbsinfo', 0, 0, 0, 0, 0, 'I(10, 1, \'Fbstatus\', \'valid\', 1, \'Fbstype\', \'fullsolve\', 1, \'Fbsmt\', \'false\', 1, \'Fbsmrhs\', \'false\', 1, \'Fbsnumcores\', \'4\', 1, \'Fbsnumsolvestotal\', \'8\', 1, \'Fbsnumsolves\', \'5\', 1, \'Fbsavgsolvetime1solvesec\', \'0.074799\', 1, \'Fbscputimesec\', \'0.373996\', 1, \'Fbsmemorytotalkb\', \'794648.000000\')', false, true)
					ProfileItem('solverprofile', 0, 0, 0, 0, 0, 'I(2, 1, \'Maxmemkb\', \'1251796\', 1, \'Maxdiskkb\', \'0\')', false, true)
				$end 'ProfileGroup'
				ProfileFootnote('I(1, 3, \'Max Mag. Delta S\', 0.0908054, \'%.5f\')', 0)
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
				ProfileItem('Adaptive Refine', 1, 0, 1, 0, 81932, 'I(1, 2, \'Tetrahedra\', 53980, false)', true, true)
				ProfileItem(' ', 0, 0, 0, 0, 0, 'I(1, 0, \'\')', false, true)
				ProfileItem('Simulation Setup ', 0, 0, 0, 0, 299452, 'I(2, 2, \'Tetrahedra\', 40346, false, 1, \'Disk\', \'26.1 KB\')', true, true)
				ProfileItem('Matrix Assembly', 1, 0, 4, 0, 667984, 'I(4, 2, \'Tetrahedra\', 40346, false, 2, \'Lumped ports\', 2, false, 2, \'P1 Triangles\', 110, false, 1, \'Disk\', \'1.18 KB\')', true, true)
				ProfileItem('Matrix Solve', 3, 0, 11, 0, 1643432, 'I(5, 1, \'Type\', \'DCS\', 2, \'Cores\', 4, false, 2, \'Matrix size\', 261514, false, 3, \'Matrix bandwidth\', 20.7011, \'%5.1f\', 1, \'Disk\', \'1.02e+03 KB\')', true, true)
				ProfileItem('Field Recovery', 1, 0, 4, 0, 1643432, 'I(3, 2, \'Excitations\', 4, false, 3, \'Average order\', 0.964742, \'%f\', 1, \'Disk\', \'2.11 MB\')', true, true)
				ProfileItem('Data Transfer', 0, 0, 0, 0, 97720, 'I(1, 0, \'Adaptive Pass 5\')', true, true)
				$begin 'ProfileGroup'
					MajorVer=2025
					MinorVer=2
					Name='APIPms'
					$begin 'StartInfo'
						I(1, 'Timesinceepock', '1754552231')
					$end 'StartInfo'
					$begin 'TotalInfo'
						I(0, ' ')
					$end 'TotalInfo'
					GroupOptions=16
					TaskDataOptions(Memory=8)
					ProfileItem('solverinfo', 0, 0, 0, 0, 0, 'I(10, 1, \'Solvertype\', \'shared_memory\', 1, \'Precision\', \'double\', 1, \'Solversymmetry\', \'complex_sym\', 1, \'Matrixdim\', \'261514\', 1, \'Matrixbw\', \'20.724100\', 1, \'Matrixnnz\', \'5419648\', 1, \'Rootdim\', \'906\', 1, \'Mathtype\', \'amd\', 1, \'Mpitasks\', \'1\', 1, \'Threadspertasks\', \'0\')', false, true)
					ProfileItem('sysinfo', 0, 0, 0, 0, 0, 'I(12, 1, \'Os\', \'win\', 1, \'Cpuid\', \'AMD Ryzen 9 8945HS w/ Radeon 780M Graphics\', 1, \'CpuPhysicCores\', \'8\', 1, \'CpuLogicCores\', \'16\', 1, \'Cpufreqkhz\', \'26510399488.000000\', 1, \'Cpucachelinesizebytes\', \'64\', 1, \'Cpuestlastlevelcachesizemb\', \'64.000000\', 1, \'Cpuestgflops\', \'524.799988\', 1, \'Memorybwestkbps\', \'51.200001\', 1, \'Numanodes\', \'1\', 1, \'Virtualmemkb\', \'137439000000.000000\', 1, \'Pagesizekb\', \'4096\')', false, true)
					ProfileItem('analysisinfo', 0, 0, 0, 0, 0, 'I(9, 1, \'Analysisstatus\', \'valid\', 1, \'Numsupernodes\', \'23267\', 1, \'Factornnz\', \'62974163\', 1, \'Factorestflops\', \'86765600000\', 1, \'Fbsestflops\', \'212645610\', 1, \'Rootfactestflops\', \'247897540\', 1, \'Rootfbsestflops\', \'410418\', 1, \'Analysistimesec\', \'1.294950\', 1, \'Analysismemkb\', \'154876.000000\')', false, true)
					ProfileItem('factorinfo', 0, 0, 0, 0, 0, 'I(4, 1, \'Fatorizationstatus\', \'valid\', 1, \'Factorizationnumcores\', \'4\', 1, \'Factorizationtimesec\', \'1.789530\', 1, \'Factorizationmentotalkb\', \'1311310.000000\')', false, true)
					ProfileItem('fbsinfo', 0, 0, 0, 0, 0, 'I(10, 1, \'Fbstatus\', \'valid\', 1, \'Fbstype\', \'fullsolve\', 1, \'Fbsmt\', \'false\', 1, \'Fbsmrhs\', \'false\', 1, \'Fbsnumcores\', \'4\', 1, \'Fbsnumsolvestotal\', \'8\', 1, \'Fbsnumsolves\', \'5\', 1, \'Fbsavgsolvetime1solvesec\', \'0.103152\', 1, \'Fbscputimesec\', \'0.515761\', 1, \'Fbsmemorytotalkb\', \'1116260.000000\')', false, true)
					ProfileItem('solverprofile', 0, 0, 0, 0, 0, 'I(2, 1, \'Maxmemkb\', \'1643432\', 1, \'Maxdiskkb\', \'0\')', false, true)
				$end 'ProfileGroup'
				ProfileFootnote('I(1, 3, \'Max Mag. Delta S\', 0.0472442, \'%.5f\')', 0)
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
				ProfileItem('Adaptive Refine', 1, 0, 1, 0, 96504, 'I(1, 2, \'Tetrahedra\', 66022, false)', true, true)
				ProfileItem(' ', 0, 0, 0, 0, 0, 'I(1, 0, \'\')', false, true)
				ProfileItem('Simulation Setup ', 0, 0, 0, 0, 327020, 'I(2, 2, \'Tetrahedra\', 51711, false, 1, \'Disk\', \'34.4 KB\')', true, true)
				ProfileItem('Matrix Assembly', 2, 0, 5, 0, 801972, 'I(4, 2, \'Tetrahedra\', 51711, false, 2, \'Lumped ports\', 2, false, 2, \'P1 Triangles\', 126, false, 1, \'Disk\', \'1.31 KB\')', true, true)
				ProfileItem('Matrix Solve', 4, 0, 15, 0, 2168380, 'I(5, 1, \'Type\', \'DCS\', 2, \'Cores\', 4, false, 2, \'Matrix size\', 334384, false, 3, \'Matrix bandwidth\', 20.9551, \'%5.1f\', 1, \'Disk\', \'1.28 MB\')', true, true)
				ProfileItem('Field Recovery', 1, 0, 5, 0, 2168380, 'I(3, 2, \'Excitations\', 4, false, 3, \'Average order\', 0.972549, \'%f\', 1, \'Disk\', \'2.61 MB\')', true, true)
				ProfileItem('Data Transfer', 0, 0, 0, 0, 97728, 'I(1, 0, \'Adaptive Pass 6\')', true, true)
				$begin 'ProfileGroup'
					MajorVer=2025
					MinorVer=2
					Name='APIPms'
					$begin 'StartInfo'
						I(1, 'Timesinceepock', '1754552244')
					$end 'StartInfo'
					$begin 'TotalInfo'
						I(0, ' ')
					$end 'TotalInfo'
					GroupOptions=16
					TaskDataOptions(Memory=8)
					ProfileItem('solverinfo', 0, 0, 0, 0, 0, 'I(10, 1, \'Solvertype\', \'shared_memory\', 1, \'Precision\', \'double\', 1, \'Solversymmetry\', \'complex_sym\', 1, \'Matrixdim\', \'334384\', 1, \'Matrixbw\', \'20.976700\', 1, \'Matrixnnz\', \'7014286\', 1, \'Rootdim\', \'1089\', 1, \'Mathtype\', \'amd\', 1, \'Mpitasks\', \'1\', 1, \'Threadspertasks\', \'0\')', false, true)
					ProfileItem('sysinfo', 0, 0, 0, 0, 0, 'I(12, 1, \'Os\', \'win\', 1, \'Cpuid\', \'AMD Ryzen 9 8945HS w/ Radeon 780M Graphics\', 1, \'CpuPhysicCores\', \'8\', 1, \'CpuLogicCores\', \'16\', 1, \'Cpufreqkhz\', \'26417399808.000000\', 1, \'Cpucachelinesizebytes\', \'64\', 1, \'Cpuestlastlevelcachesizemb\', \'64.000000\', 1, \'Cpuestgflops\', \'524.799988\', 1, \'Memorybwestkbps\', \'51.200001\', 1, \'Numanodes\', \'1\', 1, \'Virtualmemkb\', \'137439000000.000000\', 1, \'Pagesizekb\', \'4096\')', false, true)
					ProfileItem('analysisinfo', 0, 0, 0, 0, 0, 'I(9, 1, \'Analysisstatus\', \'valid\', 1, \'Numsupernodes\', \'29557\', 1, \'Factornnz\', \'87910352\', 1, \'Factorestflops\', \'132856000000\', 1, \'Fbsestflops\', \'299264013\', 1, \'Rootfactestflops\', \'430495203\', 1, \'Rootfbsestflops\', \'592960\', 1, \'Analysistimesec\', \'1.755170\', 1, \'Analysismemkb\', \'200944.000000\')', false, true)
					ProfileItem('factorinfo', 0, 0, 0, 0, 0, 'I(4, 1, \'Fatorizationstatus\', \'valid\', 1, \'Factorizationnumcores\', \'4\', 1, \'Factorizationtimesec\', \'2.610930\', 1, \'Factorizationmentotalkb\', \'1761160.000000\')', false, true)
					ProfileItem('fbsinfo', 0, 0, 0, 0, 0, 'I(10, 1, \'Fbstatus\', \'valid\', 1, \'Fbstype\', \'fullsolve\', 1, \'Fbsmt\', \'false\', 1, \'Fbsmrhs\', \'false\', 1, \'Fbsnumcores\', \'4\', 1, \'Fbsnumsolvestotal\', \'8\', 1, \'Fbsnumsolves\', \'5\', 1, \'Fbsavgsolvetime1solvesec\', \'0.135811\', 1, \'Fbscputimesec\', \'0.679056\', 1, \'Fbsmemorytotalkb\', \'1549280.000000\')', false, true)
					ProfileItem('solverprofile', 0, 0, 0, 0, 0, 'I(2, 1, \'Maxmemkb\', \'2168380\', 1, \'Maxdiskkb\', \'0\')', false, true)
				$end 'ProfileGroup'
				ProfileFootnote('I(1, 3, \'Max Mag. Delta S\', 0.0275542, \'%.5f\')', 0)
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
				ProfileItem('Adaptive Refine', 2, 0, 2, 0, 113792, 'I(1, 2, \'Tetrahedra\', 81486, false)', true, true)
				ProfileItem(' ', 0, 0, 0, 0, 0, 'I(1, 0, \'\')', false, true)
				ProfileItem('Simulation Setup ', 0, 0, 0, 0, 358728, 'I(2, 2, \'Tetrahedra\', 66242, false, 1, \'Disk\', \'38.7 KB\')', true, true)
				ProfileItem('Matrix Assembly', 3, 0, 7, 0, 967752, 'I(4, 2, \'Tetrahedra\', 66242, false, 2, \'Lumped ports\', 2, false, 2, \'P1 Triangles\', 131, false, 1, \'Disk\', \'1.33 KB\')', true, true)
				ProfileItem('Matrix Solve', 6, 0, 21, 0, 2867900, 'I(5, 1, \'Type\', \'DCS\', 2, \'Cores\', 4, false, 2, \'Matrix size\', 427694, false, 3, \'Matrix bandwidth\', 21.142, \'%5.1f\', 1, \'Disk\', \'1.63 MB\')', true, true)
				ProfileItem('Field Recovery', 1, 0, 6, 0, 2867900, 'I(3, 2, \'Excitations\', 4, false, 3, \'Average order\', 0.978624, \'%f\', 1, \'Disk\', \'3.24 MB\')', true, true)
				ProfileItem('Data Transfer', 0, 0, 0, 0, 97736, 'I(1, 0, \'Adaptive Pass 7\')', true, true)
				$begin 'ProfileGroup'
					MajorVer=2025
					MinorVer=2
					Name='APIPms'
					$begin 'StartInfo'
						I(1, 'Timesinceepock', '1754552260')
					$end 'StartInfo'
					$begin 'TotalInfo'
						I(0, ' ')
					$end 'TotalInfo'
					GroupOptions=16
					TaskDataOptions(Memory=8)
					ProfileItem('solverinfo', 0, 0, 0, 0, 0, 'I(10, 1, \'Solvertype\', \'shared_memory\', 1, \'Precision\', \'double\', 1, \'Solversymmetry\', \'complex_sym\', 1, \'Matrixdim\', \'427694\', 1, \'Matrixbw\', \'21.162901\', 1, \'Matrixnnz\', \'9051243\', 1, \'Rootdim\', \'1140\', 1, \'Mathtype\', \'amd\', 1, \'Mpitasks\', \'1\', 1, \'Threadspertasks\', \'0\')', false, true)
					ProfileItem('sysinfo', 0, 0, 0, 0, 0, 'I(12, 1, \'Os\', \'win\', 1, \'Cpuid\', \'AMD Ryzen 9 8945HS w/ Radeon 780M Graphics\', 1, \'CpuPhysicCores\', \'8\', 1, \'CpuLogicCores\', \'16\', 1, \'Cpufreqkhz\', \'26304200704.000000\', 1, \'Cpucachelinesizebytes\', \'64\', 1, \'Cpuestlastlevelcachesizemb\', \'64.000000\', 1, \'Cpuestgflops\', \'524.799988\', 1, \'Memorybwestkbps\', \'51.200001\', 1, \'Numanodes\', \'1\', 1, \'Virtualmemkb\', \'137439000000.000000\', 1, \'Pagesizekb\', \'4096\')', false, true)
					ProfileItem('analysisinfo', 0, 0, 0, 0, 0, 'I(9, 1, \'Analysisstatus\', \'valid\', 1, \'Numsupernodes\', \'37587\', 1, \'Factornnz\', \'121955385\', 1, \'Factorestflops\', \'210545000000\', 1, \'Fbsestflops\', \'413811520\', 1, \'Rootfactestflops\', \'493854198\', 1, \'Rootfbsestflops\', \'649800\', 1, \'Analysistimesec\', \'2.329290\', 1, \'Analysismemkb\', \'259560.000000\')', false, true)
					ProfileItem('factorinfo', 0, 0, 0, 0, 0, 'I(4, 1, \'Fatorizationstatus\', \'valid\', 1, \'Factorizationnumcores\', \'4\', 1, \'Factorizationtimesec\', \'3.922190\', 1, \'Factorizationmentotalkb\', \'2429070.000000\')', false, true)
					ProfileItem('fbsinfo', 0, 0, 0, 0, 0, 'I(10, 1, \'Fbstatus\', \'valid\', 1, \'Fbstype\', \'fullsolve\', 1, \'Fbsmt\', \'false\', 1, \'Fbsmrhs\', \'false\', 1, \'Fbsnumcores\', \'4\', 1, \'Fbsnumsolvestotal\', \'8\', 1, \'Fbsnumsolves\', \'5\', 1, \'Fbsavgsolvetime1solvesec\', \'0.178188\', 1, \'Fbscputimesec\', \'0.890940\', 1, \'Fbsmemorytotalkb\', \'2135800.000000\')', false, true)
					ProfileItem('solverprofile', 0, 0, 0, 0, 0, 'I(2, 1, \'Maxmemkb\', \'2867900\', 1, \'Maxdiskkb\', \'0\')', false, true)
				$end 'ProfileGroup'
				ProfileFootnote('I(1, 3, \'Max Mag. Delta S\', 0.0150446, \'%.5f\')', 0)
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
			ProfileItem('Design Validation', 0, 0, 0, 0, 0, 'I(2, 1, \'Elapsed Time\', \'00:00:00\', 1, \'Total Memory\', \'89.1 MB\')', false, true)
			ProfileItem('Initial Meshing', 0, 0, 0, 0, 0, 'I(2, 1, \'Elapsed Time\', \'00:00:22\', 1, \'Total Memory\', \'372 MB\')', false, true)
			ProfileItem('Adaptive Meshing', 0, 0, 0, 0, 0, 'I(5, 1, \'Elapsed Time\', \'00:01:09\', 1, \'Average memory/process\', \'2.73 GB\', 1, \'Max memory/process\', \'2.74 GB\', 2, \'Max number of processes/frequency\', 1, false, 2, \'Total number of cores\', 4, false)', false, true)
			ProfileFootnote('I(3, 2, \'Max solved tets\', 66242, false, 2, \'Max matrix size\', 427694, false, 1, \'Matrix bandwidth\', \'21.1\')', 0)
		$end 'ProfileGroup'
		ProfileFootnote('I(2, 1, \'Stop Time\', \'08/07/2025 15:37:44\', 1, \'Status\', \'Normal Completion\')', 0)
	$end 'ProfileGroup'
$end 'Profile'
