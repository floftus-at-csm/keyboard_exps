from PIL import Image, ImageOps
import random
from itertools import groupby

# def convolve(M, kernel):
#     height, width = size(kernel)
    
#     half_height = height ÷ 2
#     half_width = width ÷ 2
    
#     new_image = similar(M)
	
#     # (i, j) loop over the original image
# 	m, n = M.size()
#     for i in m:
#         for j in n:
#             # (k, l) loop over the neighbouring pixels
# 			accumulator = 0 * M[1, 1]
# 			for k in -half_height:-half_height + height - 1:
# 				for l in -half_width:-half_width + width - 1:
# 					Mi = i - k
# 					Mj = j - l
# 					# First index into M
# 					if Mi < 1:
# 						Mi = 1
# 					else if Mi > m:
# 						Mi = m
# 					end
# 					# Second index into M
# 					if Mj < 1:
# 						Mj = 1
# 					else if Mj > n:
# 						Mj = n
# 					accumulator += kernel[k, l] * M[Mi, Mj]
# 			new_image[i, j] = accumulator
#     return new_image


# ============================================#

def split_string(a):
	split_sample = a.split()
	char_array = []
	for i in split_sample:
		characters = split(i)
		char_array.append(characters)
	return char_array

# ============================================#

def step_image(M, word_size):
    # this function should return locations that words of a specific length can be put at
	# I already feel that this is the 'greedy' way of doing this
    # new_text_image = similar(M)
	# THIS NEEDS TO CHANGE
	# It feels way too expensive - I could just do this for every length of word? 
	x_y_coords = []
    # (i, j) loop over the original image
	h = M.height
	w = M.width
	for y in range(h):
		for x in range(w):
			value = 0
			for z in range(word_size):
				try:
					# print(M.getpixel((y, x+z)))
					if M.getpixel((x+z, y)) < 1:
						# then its black
						value=value+1
				except:
					print("at end of line")

			
			if value == word_size:
				x_y_coords.append([x, y])
	return x_y_coords

# ============================================#

def order_the_words(word_l, char_set, strings):
	ordered_s = []
	for j in range(word_l):
		val = 0 
		temp_v = []
		for i in char_set:
			# print(i)
			# print(len(i))
			# print(strings[val])
			if len(i) == j:
				print("in if")
				temp_v.append(strings[val])
				print(temp_v)
			val+=1
	print(temp_v)
	ordered_s.append(temp_v)
	return ordered_s

# ============================================#

def get_coords(word_l, m):
	entire_coords = []
	for i in range(word_l):
		t_v = step_image(m, i)
		entire_coords.append(t_v)
	return entire_coords

# ============================================#

def iterate_through(full_xy_coords, word_l, m, ordered):
	h = m.height
	w = m.width
	val = word_l
	pause = 0
	temp_w = ""
	trigger2 = False
	for i in range(h):
		for j in range(w):
			trigger = False
			trigger2 = False
			if pause > 0:
				pause = pause - 1
			else:
				# for z in word_l:-1:1
				for z in range(word_l-1, 1, -1):
					t = [j, i]
					if trigger2 == False:
						if t in full_xy_coords[z]:
							if len(ordered[z-1]) > 0:
								# ordered is the words split into characters ordered
								r = random.randint(0, len(ordered[z-1])-1)
								temp_w = temp_w + ordered[z-1][r]
								pause = z - 1
								trigger2 = True
				if trigger == False and trigger2 == False:
						# this doesn't need to be a space - it could be anything - like binary
						temp_w = temp_w + " " 
			if j == w-1:
					temp_w = temp_w + "\n"
					print("line break")
					pause = 0
	return temp_w

# Python3 program to Split string into characters
def split(word):
    return [char for char in word]
# ============================================#	
ordered_letters = "8@GW9BAHNRX4560EMPQSYZmagDFKO7enswCJTV23bfkdpqtxyzILU1horuv?cjl!i.,-_"
split_letters = ordered_letters.split()
print(split_letters)
im = Image.open("images/superflux2.png")
new_width = 100
percentage_scale = new_width / im.width
# im_resized = im.resize((im.width*percentage_scale, im.height*percentage_scale))
im_resized = im.resize((100, 60))
# im_grayscale = ImageOps.grayscale(im_resized)
im_resized = im_resized.convert('L')
threshold = 120
im_resized = im_resized.point( lambda p: 255 if p>threshold else 0)
im_resized = im_resized.convert('1')
im_resized.show()
sample_text = "we promise to wake you up if we think you won't get the point of the dream. we promise to show up if you show up."
# chars = split(ordered_letters)
chars = split_string(sample_text)
strings_vec = sample_text.split()
# print(type(strings_vec))
# print(len(strings_vec[1]))
print(chars)
print(strings_vec)

longest_word = 0
for i in strings_vec:
	# print(i)
	if len(i) > longest_word:
		longest_word = len(i)
print("the longest word is: ", longest_word)
# strings_vec = sample_text.split()

# # alt method
# ordered_string_vec = []
# for j in longest_word:
# 	val=1
# 	temp_vec = []
# 	for i in chars:
# 		if len(i) == j
# 			temp_vec.append(strings_vec[val])
# 		val+=1
# ordered_string_vec.append(temp_vec)	


# get_coords(longest_word, im_resized)

# word = "hello"
# ordered_l = order_the_words(longest_word, chars, strings_vec)
strings_vec.sort(key=len, reverse=False) # sorts by descending length
chars.sort(key=len, reverse=False)
print(chars)
# print(strings_vec)
# word = string(word, ordered_l[2][1])

# # this now works but i've somehow got my x,y wrong
the_coords = get_coords(longest_word, im_resized)
print(the_coords)
# ordered_w = order_the_words(longest_word, chars, strings_vec)
ordered_w = [list(set(items)) for length, items in groupby(strings_vec, key=len)]
print(ordered_w)

final_string_image = iterate_through(the_coords, longest_word, im_resized, ordered_w)
print(final_string_image)

# split_lines = final_string_image.splitlines()
# print(split_lines)
with open("text_images/test.txt", "a") as myfile:
	myfile.write(final_string_image)
# 	for line in split_lines:
# 		myfile.write(line+'\n')
# # io = open("file28.txt", "w")
# # println(io, final_string_image)
# # close(io)

# wo, hi = img_binary.size()