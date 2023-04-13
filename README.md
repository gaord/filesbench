# filesbench做什么？
提供对于海量小文件的读写性能测试工具代码，可以用于多种文件系统，包括ext4、xfs、btrfs、zfs、glusterfs、ceph等的相关场景的性能测试。

# 如何使用？
在需要测试的存储介质上创建一个目标目录，比如/mnt/cephfs/filesbench，进入这个目录，然后执行：
```
python3 generate_files.py
```
测试海量小文件将在当前目录下随机生成。

如下测试小文件读写性能：
```
python3 randrwbench.py --working_dir /mnt/cephfs/filesbench
```

当前目录下会产生测试结果数据文件，performance_log_timestamp.json。例子如下：
```
	{
		"directory": "./10w5g4d/dir_4345",
		"results": [
			{
				"file_name": "file_4946.txt",
				"file_path": "./10w5g4d/dir_4345/dir_3006/dir_1046/file_4946.txt",
				"file_size": 944,
				"read_time": 0.006720781326293945,
				"write_time": 0.010959625244140625
			}
		],
		"max_read_time": 0.006720781326293945,
		"min_read_time": 0.006720781326293945,
		"avg_read_time": 0.006720781326293945,
		"max_write_time": 0.010959625244140625,
		"min_write_time": 0.010959625244140625,
		"avg_write_time": 0.010959625244140625
	},
	{
		"directory": "./10w5g4d/dir_4344",
		"results": [
			{
				"file_name": "file_2120.txt",
				"file_path": "./10w5g4d/dir_4344/dir_525/file_2120.txt",
				"file_size": 6708,
				"read_time": 0.002254962921142578,
				"write_time": 0.013688087463378906
			}
		],
		"max_read_time": 0.002254962921142578,
		"min_read_time": 0.002254962921142578,
		"avg_read_time": 0.002254962921142578,
		"max_write_time": 0.013688087463378906,
		"min_write_time": 0.013688087463378906,
		"avg_write_time": 0.013688087463378906
	}
‘’‘