import random
import sys
import os
class Player67():
	def __init__(self):
		self.playerFlag=0;
		self.opFlag=0;
		self.moves=0;
		pass

	def move(self, board, old_move, flag):
		if(self.playerFlag==0 and flag=='x'):
			self.moves=-1;
			#print self.moves;
		elif(self.playerFlag==0 and flag=='o'):
			self.moves=0;
		self.playerFlag=flag;
		#print self.playerFlag;
		if(flag=='x'):
			self.opFlag='o';
		else:
			self.opFlag='x';
		self.moves=self.moves+2;
		if(self.moves==1):
			cells = board.find_valid_move_cells(old_move)
			return cells[random.randrange(len(cells))]
		else:
			values_child=[];
			ans=self.mini_max(board, old_move, flag,1,1,-10000000000,100000000,values_child)
			for value in values_child:
				if value[0]==ans:
					x=value[1];
					y=value[2];
					break;
			return (int(x),int(y))

	def mini_max(self,board, old_move, flag,depth,cnt,alpha,beta,values_child):
		
		if depth==3:
			if self.playerFlag=='x':
				compflag='o';
			else:
				compflag='x';
			return self.heuristic(board,self.playerFlag,compflag);
		else:
			cells=board.find_valid_move_cells(old_move);
			if cnt%2==1:
				maxi=-10000000
				for move in cells:
					board.board_status[move[0]][move[1]]=flag;
					temp=self.mini_max(board,move,self.opFlag,depth+1,cnt+1,alpha,beta,values_child);
					if(depth==1):
						values_child.append((temp,move[0],move[1]));
					maxi=max(maxi,temp);
					board.board_status[move[0]][move[1]]='-';
					alpha=max(alpha,maxi);
					if beta<=alpha:
						break;
				return maxi
			else:
				mini=10000000
				for move in cells:
					board.board_status[move[0]][move[1]]=flag;
					mini=min(mini,self.mini_max(board,move,self.playerFlag,depth+1,cnt+1,alpha,beta,values_child))
					board.board_status[move[0]][move[1]]='-';
					beta=min(mini,beta);
					if beta<=alpha:
						break;
				return mini
	def max(a,b):
		if(a>b):
			return a;
		else:
			return b;
	def min(a,b):
		if(a>b):
			return b;
		else:
			return a;

	def heuristic(self,board,flag,compflag):
		util_values = [0 for i in range(16)]
		for i in range(16):
			util_values[i] = self.calc_utility(board, i, flag)
		gain = 0
		lim = 100.0
		for i in range(16):
			util_values[i] /= lim
		
		for i in range(4):
			p = 0
			cp = 0
			ce = 0
			for j in range(4):
				p += util_values[j * 4 + i]
				if board.block_status[j][i] == flag:
					cp += 1
				elif board.block_status[j][i] == compflag:
					ce += 1
			gain = self.get_factor(p, gain)
			gain = self.get_new1(cp, ce, gain)
		#print gain;
		for j in range(4):
			p = 0
			cp = 0
			ce = 0
			for i in range(4):
				p += util_values[j * 4 + i]
				if board.block_status[j][i] == flag:
					cp += 1
				elif board.block_status[j][i] ==compflag:
					ce += 1
			gain = self.get_factor(p, gain)
			gain = self.get_new1(cp, ce, gain)
			p = 0
			cp = 0
			ce = 0
			for i in range(4):
				p+= util_values[4 * i + i]
				if board.block_status[i][i] == flag:
					cp += 1
				elif board.block_status[i][i] ==compflag:
					ce += 1
			gain = self.get_factor(p, gain)
			gain = self.get_new1(cp, ce, gain)

		p = 0
		cp = 0
		ce = 0
		for i in range(1, 5):
			p += util_values[3 * i]
			if board.block_status[i-1][4-i] == flag:
				cp += 1
			elif board.block_status[i-1][4-i] == compflag:
				ce += 1
		gain = self.get_new1(cp, ce, gain)
		gain = self.get_factor(p, gain)

		# if self.cntp < 2:
		# 	if board.block_status[4] == flag:
		# 		gain += 10
		# 	elif board.block_status[4] != '-':
		# 		gain -= 10
		# cnt1 = board.block_status.count(flag)
		# cnt2 = board.block_status.count(compflag)
		# # if self.cntp < cnt1 and cnt2 == self.cnto:
		# 	gain += 50
		# elif cnt1 > self.cntp and (cnt1 - self.cntp) < (cnt2 - self.cnto):
		# 	gain -= 20
		# elif cnt1 < self.cntp and cnt2 > self.cnto:
		# 	gain -= 50
		return gain

	def calc_utility(self, board, boardno,flag):
		gain = 0
		startx = boardno / 4
		starty = boardno % 4
		starty *= 4
		startx *= 4
		for i in range(startx, startx + 4):
			cp = 0
			ce = 0
			cd = 0
			for j in range(starty, starty + 4):
				if board.board_status[i][j] == '-':
					cd += 1
				elif board.board_status[i][j] == flag:
					cp += 1
				else:
					ce += 1
			gain = self.calc1(cp, ce, gain,boardno)

		for j in range(starty, starty + 4):
			cp = 0
			ce = 0
			cd = 0
			for i in range(startx, startx + 4):
				if board.board_status[i][j] == '-':
					cd += 1
				elif board.board_status[i][j] == flag:
					cp += 1
				else:
					ce += 1
			gain = self.calc1(cp, ce, gain,boardno)
		cp = 0
		cd = 0
		ce = 0
		for i in range(0, 4):
			if board.board_status[startx + i][starty + i] == flag:
				cp += 1
			elif board.board_status[startx + i][starty + i] == '-':
				cd += 1
			else:
				ce += 1
		gain = self.calc1(cp, ce, gain,boardno)
		for i in range(0, 4):
   			if board.board_status[startx + i][starty + 3 - i] == flag:
				cp += 1
			elif board.board_status[startx + i][starty + 3 - i] == '-':
				cd += 1
			else:
				ce += 1
		gain = self.calc1(cp, ce, gain,boardno)
		return gain

	
	def calc1(self,cx,co,gain,boardno):
		if cx == 4:
			gain += 10000
		if cx == 3:
			if co==1:
				gain-=0;
			else:
				gain+=1000;
		if cx == 2:
			if co>=1:
				gain-=0;
			else:
				gain +=100
		if cx==1:
			if co==3:
				gain+=10000;
			elif co==2:
				gain+=1000;
			elif co==1:
				gain+=100;
			elif co==0:
				gain+=0;
		if co == 4:
			gain -= 10000
		if co == 3:
			if cx==0:
				gain-=1000;
		if co == 2:
			if cx==0:
				gain-=100;
		if co==1:
			if cx==0:
				gain+=10;
		return gain
	
		
	def get_factor(self, p, gain):
		if p < 1 and p >= -1:
			gain += p
		if p >= 1 and p < 2:
			val = 1
			val += (p - 1) * 9
			gain += val
		if p >= 2 and p < 3:
			val = 10
			val += (p - 1) * 90
			gain += val
		if p >= 3:
			val = 100
			val += (p - 3) * 900
			gain += val
		if p >= -2 and p < -1:
			val = -1
			val -= (abs(p) - 1) * 9
			gain += val
		if p >= -3 and p < -2:
			val = -10
			val -= (abs(p) - 2) * 90
			gain += val
		if p < -3:
			val = -100
			val -= (abs(p) - 3) * 900
			gain += val
		return gain

	
	def get_new1(self,cx,co,gain):
		if cx == 4:
			gain += 10000
		if cx == 3:
			if co==1:
				gain-=0;
			else:
				gain+=1000;
		if cx == 2:
			if co>=1:
				gain-=0;
			else:
				gain +=100
		if cx==1:
			if co==3:
				gain+=10000;
			elif co==2:
				gain+=1000;
			elif co==1:
				gain+=100;
			elif co==0:
				gain+=0;
		if co == 4:
			gain -= 10000
		if co == 3:
			if cx==0:
				gain-=1000;
		if co == 2:
			if cx==0:
				gain-=100;
		if co==1:
			if cx==0:
				gain+=10;
		return gain