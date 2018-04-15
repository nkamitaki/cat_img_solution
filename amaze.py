import hashlib
sha256 = lambda s: hashlib.sha256(path).digest()

b32 = lambda x: int(0xFFFFFFFF & x)

mtindex = 624
mt = [0] * 624
mt[0] = 42
for i in range(1, 624):
	mt[i] = b32(1812433253 * (mt[i - 1] ^ mt[i - 1] >> 30) + i)

def mtget():
	global mtindex
	global mt

	if mtindex >= 624:
		for i in range(624):
			y = b32((mt[i] & 0x80000000) +
				(mt[(i + 1) % 624] & 0x7fffffff))
			mt[i] = mt[(i + 397) % 624] ^ y >> 1
			if y % 2 != 0:
				mt[i] = mt[i] ^ 0x9908b0df
		mtindex = 0

	y = mt[mtindex]
	y = y ^ y >> 11
	y = y ^ y << 7 & 2636928640
	y = y ^ y << 15 & 4022730752
	y = y ^ y >> 18
	mtindex += 1
	return b32(y)


size = 9*2+1
maze = [[[0]*size for i in range(size)] for i in range(size)]

def getM(s):
	return maze[s[0]][s[1]][s[2]]
def setM(s, v):
	maze[s[0]][s[1]][s[2]] = v

isWall  = lambda s: min(s) >= 0 and max(s) < size and getM(s) == 0
isSpace = lambda s: min(s) >= 0 and max(s) < size and getM(s) != 0


directions = \
[
lambda s: (s[0]-1, s[1]  , s[2]  ),
lambda s: (s[0]+1, s[1]  , s[2]  ),
lambda s: (s[0]  , s[1]-1, s[2]  ),
lambda s: (s[0]  , s[1]+1, s[2]  ),
lambda s: (s[0]  , s[1]  , s[2]-1),
lambda s: (s[0]  , s[1]  , s[2]+1)
]


stack = [(1,1,1)]
setM(stack[0], 1)

def makeNext():
	pos = stack[-1]
	available = [d for d in directions if isWall(d(d(pos)))]
	d = available[mtget() % len(available)]
	pos = d(pos)
	setM(pos, len(stack))
	pos = d(pos)
	stack.append(pos)
	setM(pos, len(stack))

def makeMaze():
	while len(stack) > 0:
		try:
			makeNext()
		except:
			stack.pop(-1)


def testPath(path):
	pos = (size-2,size-2,size-2)
	good = True
	for step in path:
		d = directions[int(step)]
		pos = d(pos)
		good = good and isSpace(pos)
		pos = d(pos)
		good = good and isSpace(pos)
	return good and pos == (1,1,1)



if __name__ == '__main__':
	makeMaze()
	path = raw_input().strip()
	if not testPath(path):
		raise Exception()
	h = sha256(sha256(path))
	mask = [225, 38, 235, 89, 101, 61, 53, 254, 173, 180, 141, 92, 9, 88, 26, 64, 231, 157, 56, 210, 61, 222, 220, 160, 167, 129, 115, 247, 137, 218]
	print ''.join([chr(ord(h[i]) ^ mask[i]) for i in range(len(mask))])

