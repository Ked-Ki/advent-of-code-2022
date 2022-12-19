import util.logging as log

from util.moreiters import consume, batch_at


class FileTreeNode:
    def __init__(self, name):
        self.name = name
        self.files = {}
        self.dirs = {}
        self.total_size = 0

    def insert_file(self, name, size):
        self.files[name] = size

    def insert_dir(self, name):
        if name not in self.dirs:
            self.dirs[name] = FileTreeNode(name)

    def incr_size(self, size):
        self.total_size += size

    def traverse_dirs(self):
        yield self
        for d in self.dirs.values():
            yield from d.traverse_dirs()

    def __repr__(self):
        return (
            f"FileTreeNode({self.name},files={list(self.files.keys())},"
            + f"dirs={list(self.dirs.keys())},total_size={self.total_size})"
        )


def build_file_tree(lines):
    cur_path = []
    root_node = None
    for cmd_l in batch_at(iter(lines), lambda s: s[0] == "$"):
        cmd = next(cmd_l).split()
        log.parse_log.debug(f"{cur_path=}, {cmd=}")
        if cmd[1] == "cd":
            folder = cmd[2]
            if folder == "..":
                cur_path = cur_path[:-1]
            else:
                if cur_path:
                    cur_path[-1].insert_dir(folder)
                    cur_path.append(cur_path[-1].dirs[folder])
                else:
                    root_node = FileTreeNode(folder)
                    cur_path.append(root_node)
            consume(cmd_l)
        elif cmd[1] == "ls":
            for ls_entry in cmd_l:
                entry_words = ls_entry.split()
                if entry_words[0] == "dir":
                    cur_path[-1].insert_dir(entry_words[1])
                else:
                    size = int(entry_words[0])
                    cur_path[-1].insert_file(name=entry_words[1], size=size)
                    for node in cur_path:
                        node.incr_size(size)
    return root_node


def part1(lines, **_kw_args):
    file_tree = build_file_tree(lines)

    return sum(
        size for d in file_tree.traverse_dirs() if (size := d.total_size) <= 100000
    )


def part2(lines, **_kw_args):
    file_tree = build_file_tree(lines)

    total_space = 70000000
    total_needed_space = 30000000
    available_space = total_space - file_tree.total_size

    space_to_delete = total_needed_space - available_space

    return min(
        size
        for d in file_tree.traverse_dirs()
        if (size := d.total_size) >= space_to_delete
    )
