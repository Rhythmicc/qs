"""
针对Mac的磁盘挂载和卸载工具
"""
import subprocess


class DMG:
    """
    针对Mac的磁盘挂载和卸载工具
    """
    def __init__(self):
        self.disk_info = []

    def mount(self, path):
        """
        挂载磁盘
        """
        subprocess.run(['hdiutil', 'attach', path])

    def unmount(self, path):
        """
        卸载磁盘
        """
        subprocess.run(['hdiutil', 'detach', path])

    def get_disk_list(self):
        """
        获取磁盘列表
        """
        disk_list = subprocess.run(['diskutil', 'list'], stdout=subprocess.PIPE).stdout.decode().split('\n\n')
        for item in disk_list:
            item_info = item.split('\n')
            _ls = item_info[0].strip().split()
            if not _ls:
                continue
            path, disk_type = _ls[0], ' '.join(_ls[1:])
            disk_type = disk_type.strip('(').strip('):')
            disk_size = 0
            for line in item_info[1:]:
                if line.strip().startswith('0'):
                    disk_size = ' '.join(line.strip().split()[-3:-1])
                    break
            self.disk_info.append({
                'path': path,
                'type': disk_type,
                'size': disk_size
            })
        return self.disk_info


if __name__ == '__main__':
    from .. import qs_default_console
    disk = Disk()
    qs_default_console.print(disk.get_disk_list())
