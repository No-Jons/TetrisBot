import random
import copy


class Game:
    def __init__(self, monochrome: bool = False):
        self.monochrome = monochrome
        self.width = 10
        self.height = 16
        self.board = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.pieces = [
            {
                "id": "a_l1",  # orange
                "shape": [(1, 1), (1, 0), (0, 0), (-1, 0)],
                "pos": [1, 4],
                "rotations": {
                    0: [(1, 1), (1, 0), (0, 0), (-1, 0)],
                    90: [(1, -1), (0, 1), (0, 0), (0, -1)],
                    180: [(-1, -1), (1, 0), (0, 0), (-1, 0)],
                    270: [(-1, 1), (0, -1), (0, 0), (0, 1)]
                },
                "rotation": 0
            },
            {
                "id": "a_l2",  # blue
                "shape": [(1, -1), (1, 0), (0, 0), (-1, 0)],
                "pos": [1, 5],
                "rotations": {
                    0: [(1, -1), (1, 0), (0, 0), (-1, 0)],
                    90: [(-1, -1), (0, 1), (0, 0), (0, -1)],
                    180: [(-1, 1), (1, 0), (0, 0), (-1, 0)],
                    270: [(1, 1), (0, -1), (0, 0), (0, 1)]
                },
                "rotation": 0
            },
            {
                "id": "a_line",  # yellow
                "shape": [(-1, 0), (0, 0), (1, 0), (2, 0)],
                "pos": [1, 4],
                "rotations": {
                    0: [(-1, 0), (0, 0), (1, 0), (2, 0)],
                    90: [(0, -1), (0, 0), (0, 1), (0, 2)],
                    180: [(-1, 0), (0, 0), (1, 0), (2, 0)],
                    270: [(0, -1), (0, 0), (0, 1), (0, 2)]
                },
                "rotation": 0
            },
            {
                "id": "a_t",  # purple
                "shape": [(0, 1), (0, 0), (0, -1), (1, 0)],
                "pos": [1, 4],
                "rotations": {
                    0: [(0, 1), (0, 0), (0, -1), (1, 0)],
                    90: [(0, -1), (0, 0), (-1, 0), (1, 0)],
                    180: [(0, -1), (0, 0), (0, 1), (-1, 0)],
                    270: [(0, 0), (0, 1), (-1, 0), (1, 0)]
                },
                "rotation": 0
            },
            {
                "id": "a_square",  # red
                "shape": [(0, 0), (0, 1), (1, 0), (1, 1)],
                "pos": [1, 4],
                "rotations": {
                    0: [(0, 0), (0, 1), (1, 0), (1, 1)],
                    90: [(0, 0), (0, 1), (1, 0), (1, 1)],
                    180: [(0, 0), (0, 1), (1, 0), (1, 1)],
                    270: [(0, 0), (0, 1), (1, 0), (1, 1)]
                },
                "rotation": 0
            },
            {
                "id": "a_s1",  # green
                "shape": [(1, 1), (0, 1), (0, 0), (-1, 0)],
                "pos": [1, 4],
                "rotations": {
                    0: [(1, 1), (0, 1), (0, 0), (-1, 0)],
                    90: [(1, -1), (1, 0), (0, 0), (0, 1)],
                    180: [(1, 1), (0, 1), (0, 0), (-1, 0)],
                    270: [(1, -1), (1, 0), (0, 0), (0, 1)]
                },
                "rotation": 0
            },
            {
                "id": "a_s2",  # brown
                "shape": [(-1, 0), (0, 0), (0, -1), (1, -1)],
                "pos": [1, 5],
                "rotations": {
                    0: [(-1, 0), (0, 0), (0, -1), (1, -1)],
                    90: [(0, -1), (0, 0), (1, 0), (1, 1)],
                    180: [(-1, 0), (0, 0), (0, -1), (1, -1)],
                    270: [(0, -1), (0, 0), (1, 0), (1, 1)]
                },
                "rotation": 0
            }
        ]
        self.current_piece = copy.deepcopy(random.choice(self.pieces))
        self.next_piece = copy.deepcopy(random.choice(self.pieces))
        self._render_piece(self.current_piece, self.current_piece["pos"])
        self.emojis = {
            "default": "⬛",
            "l1": "🟧",
            "l2": "🟦",
            "line": "🟨",
            "t": "🟪",
            "square": "🟥",
            "s1": "🟩",
            "s2": "🟫",
            "hl": "🔳",
            "mono": "⬜"
        }
        self.lines = 0

    def _render_piece(self, piece, pos, emoji_id: str = None):
        for grid in piece["shape"]:
            if emoji_id:
                self.board[pos[0] + grid[0]][pos[1] + grid[1]] = emoji_id
            else:
                self.board[pos[0] + grid[0]][pos[1] + grid[1]] = piece["id"]
            
    def _remove_piece(self, piece, pos):
        for grid in piece["shape"]:
            self.board[pos[0] + grid[0]][pos[1] + grid[1]] = None

    def _get_grids(self, piece, pos):
        grids = list()
        for grid in piece["shape"]:
            try:
                grids.append(self.board[pos[0] + grid[0]][pos[1] + grid[1]])
            except IndexError:
                grids.append("ground")
        return grids

    @staticmethod
    def _get_placements(piece, pos):
        placements = list()
        for place in piece["shape"]:
            placements.append((pos[0] + place[0], pos[1] + place[1]))
        return placements

    def _change_pieces(self):
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if str(self.board[y][x]).startswith("a_"):
                    self.board[y][x] = self.board[y][x].replace("a_", "")
        self.current_piece = self.next_piece
        self.next_piece = copy.deepcopy(random.choice(self.pieces))
        for y in range(len(self.board)):
            line = self.board[y]
            if None not in line:
                self.lines += 1
                self.board.pop(y)
                self.board.insert(0, [None for _ in range(self.width)])
        if self._get_grids(self.current_piece, self.current_piece["pos"]) != \
                [None for _ in range(len(self.current_piece["shape"]))]:
            return True
        return False

    def _render_highlight(self):
        for push in range(int(self.current_piece["pos"][0]), self.height + 1):
            hit = False
            for grid in self._get_grids(self.current_piece, (push, self.current_piece["pos"][1])):
                if grid is not None and grid != self.current_piece["id"] and grid != "hl":
                    hit = True
                    break
            if hit:
                push -= 1
                self._render_piece(self.current_piece, (push, self.current_piece["pos"][1]), emoji_id="hl")
                break

    def _remove_highlight(self):
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] == "hl":
                    self.board[y][x] = None

    def increment(self):
        self._remove_highlight()
        self._remove_piece(self.current_piece, self.current_piece["pos"])
        pos = (int(self.current_piece["pos"][0]) + 1, self.current_piece["pos"][1])
        grounded = False
        hit_block = False
        loss = False
        if self._get_grids(self.current_piece, pos) != \
                [None for _ in range(len(self.current_piece["shape"]))]:
            grounded = True
            hit_block = True
        if not grounded:
            for place in self._get_placements(self.current_piece, self.current_piece["pos"]):
                if place[0] == (self.height - 1):
                    grounded = True
        if grounded:
            if not hit_block:
                self.current_piece["pos"][0] += 1
            self._render_piece(self.current_piece, self.current_piece["pos"])
            loss = self._change_pieces()
        else:
            self.current_piece["pos"][0] += 1
        if not loss:
            self._render_highlight()
        self._render_piece(self.current_piece, self.current_piece["pos"])
        return loss

    def do_action(self, emoji):
        do_render = False
        start_pos = copy.deepcopy(self.current_piece["pos"])
        if emoji == "⬅️":
            hit = False
            for place in self._get_placements(self.current_piece, self.current_piece["pos"]):
                if place[1] == 0:
                    hit = True
            new_pos = (self.current_piece["pos"][0], int(self.current_piece["pos"][1]) - 1)
            for grid in self._get_grids(self.current_piece, new_pos):
                if grid is not None and grid != self.current_piece["id"] and grid != "hl":
                    hit = True
            if not hit:
                do_render = True
                self.current_piece["pos"][1] -= 1
        if emoji == "➡️":
            hit = False
            for place in self._get_placements(self.current_piece, self.current_piece["pos"]):
                if place[1] == (self.width - 1):
                    hit = True
            new_pos = (self.current_piece["pos"][0], int(self.current_piece["pos"][1]) + 1)
            for grid in self._get_grids(self.current_piece, new_pos):
                if grid is not None and not grid == self.current_piece["id"] and grid != "hl":
                    hit = True
            if not hit:
                do_render = True
                self.current_piece["pos"][1] += 1
        if emoji == "⬇️":
            start_pos = self.current_piece["pos"]
            for push in range(self.height - int(self.current_piece["pos"][0]) + 1):
                hit = False
                new_pos = (int(self.current_piece["pos"][0]) + push, self.current_piece["pos"][1])
                for grid in self._get_grids(self.current_piece, new_pos):
                    if grid is not None and grid is not self.current_piece["id"] and grid != "hl":
                        hit = True
                if hit:
                    do_render = True
                    self._remove_piece(self.current_piece, start_pos)
                    self.current_piece["pos"][0] += push - 1
                    break
        if emoji == "↩️":
            dummy = copy.deepcopy(self.current_piece)
            rotated = False
            for _ in range(360 // 90):
                dummy["rotation"] += 90 if (dummy["rotation"] != 270) else -270
                dummy["shape"] = dummy["rotations"][dummy["rotation"]]
                valid_spaces = list()
                for place in self._get_placements(dummy, dummy["pos"]):
                    if 0 <= place[0] <= (self.height - 1) and 0 <= place[1] <= (self.width - 1):
                        valid_spaces.append(True)
                    else:
                        valid_spaces.append(False)
                if valid_spaces == [True for _ in dummy["shape"]]:
                    rotated = True
                    break
                    # todo: fix rotate into other grids bug
            if rotated:
                do_render = True
                self._remove_piece(self.current_piece, start_pos)
                self.current_piece["rotation"] = dummy["rotation"]
                self.current_piece["shape"] = dummy["shape"]
        if do_render:
            self._remove_piece(self.current_piece, start_pos)
            self._render_piece(self.current_piece, self.current_piece["pos"])

    def render(self):
        output = "```\n"
        for line in self.board:
            for grid in line:
                if grid is None:
                    output += self.emojis["default"]
                elif isinstance(grid, str):
                    if self.monochrome:
                        if grid == "hl":
                            output += self.emojis["hl"]
                        else:

                            output += self.emojis["mono"]
                    else:
                        output += self.emojis[grid.replace("a_", "")]
            output += "\n"
        return output + "```"
