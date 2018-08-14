#https://github.com/ppakotze/python

def booklet_p(n):
 #return a text string list of pages for booklet printing
 half=n//2
 page_list=[n]
 for x in range(1,half,2):
   page_list+=([x, x+1, n-x, n-x-1])
 return(str(page_list[:-1]))

#10, 3, 4, 9, 8, 5, 6, 7, 2

#16, 1, 2, 15, 14, 3, 4, 13, 12, 5, 6, 11, 10, 7, 8, 9
