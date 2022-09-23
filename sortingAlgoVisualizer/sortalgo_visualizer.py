
from heapq import heapify, heappop
import tkinter as tk
import time
import random

width = 1100
height = 700
buttonWidth = .1
buttonHeight = .05
size = 20

vals = [None] * size
bars = [None] * size
sortSpeed = 300
interrupted = False
sorting = False
defaultColor = '#4C4E52'
selectColor = '#1e847f'
currTime = 0
mergeQueue = []
quickQueue = []


root = tk.Tk()
root.title("Sort Algorithm Visualizer")

canvas = tk.Canvas(root, height = height, width = width, bg = '#ecc19c')
canvas.pack()

#sorting algorithms

#1) QUICKSORT

def quicksortAnimation(step, prev = False, idx1 = None, idx2 = None, swapNums = False): #helper method for quicksort
    global interrupted, sorting, quickQueue, sortSpeed, size
    if (not quickQueue and step==1) or interrupted:
        if prev: 
            changeColor(prev[0], defaultColor)
            changeColor(prev[1],defaultColor)
        buttonColor(quicksort,False)
        interrupted = False 
        sorting = False
        quickQueue = []
        return

    if step == 1:
        if prev: 
            changeColor(prev[0], defaultColor)
            changeColor(prev[1],defaultColor)
        
        indices = quickQueue.pop(0)
        idx1 = indices[0]
        idx2 = indices[1]
        swapNums = indices[2]
        changeColor(idx1, selectColor)
        changeColor(idx2, selectColor)
        if size >= 200 and not swapNums:
            root.after(0, lambda:quicksortAnimation(1, (idx1,idx2)))
        else:
            root.after(sortSpeed, lambda: quicksortAnimation(2, None, idx1, idx2, swapNums))
    elif swapNums:
        swap(idx1, idx2)
        updateScreen()
        changeColor(idx1, selectColor)
        changeColor(idx2, selectColor)
        root.after(sortSpeed,lambda: quicksortAnimation(1, (idx1, idx2)))
    else:
        root.after(0, lambda: quicksortAnimation(1, (idx1, idx2)))
    
def quicksort(list = None, newSort = True, start = 0, end = 0):
    global interrupted, sorting, vals
    if sorting and newSort:
        return
    elif newSort: 
        sorting = True
        buttonColor(quicksort, True)
        list = vals[:]
        end = size
    
    #Quicksort Algo

    if end - start <= 1:
        return
    
    pivot = list[end - 1]
    left = start
    right = end - 2
    while left < right:
        if list[left] > pivot and list[right] < pivot:
            quickQueue.append([left, right, True])
            list[left] = list[right]
            list[right] = list[left]
            left += 1
            right -= 1
        elif list[left] > pivot:
            quickQueue.append([left, right, False])
            right -= 1
        elif list[right] < pivot:
            quickQueue.append([left, right, False])
            left += 1
        else:
            quickQueue.append([left, right, False])
            left += 1 
            right -= 1

    switchIndices = right + 1 if list[right] < pivot else right
    list[switchIndices] = list[end - 1]
    list[end - 1] = list[switchIndices]
    quickQueue.append([switchIndices, end - 1, True])

    quicksort(list, False, start, switchIndices)
    quicksort(list, False, switchIndices + 1, end)

    if end == size and start == 0:
        quicksortAnimation(1)

#3) MERGE SORT

def shiftRight(indices): #merge helper method
    global vals
    for i in indices: 
        vals[i] = vals[i - 1]

def mergeAnimation(newStep = True, positions = False, prev = None, newComparison = True):
    global interrupted, sorting, vals, mergeQueue
    if (not mergeQueue and not positions) or interrupted:
        buttonColor(merge,False)
        interrupted = False
        sorting = False
        mergeQueue = []
        return
    
    if newStep:
        positions = mergeQueue.pop(0)
    if newComparison:
        left = positions[0]
        right = positions[1]
        lstart = positions[2]
        rstart = positions[3]
        changeColor(prev,defaultColor) if type(prev) == int else False
        changeColor(lstart, selectColor) if left else False
        changeColor(rstart, selectColor) if right else False
        scalingSpeed = 0 if size >=200 and sortSpeed <= 1 else sortSpeed
        root.after(scalingSpeed, lambda: mergeAnimation(False,positions,None,False))
    else:
        left = positions[0]
        right = positions[1]
        lstart = positions[2]
        rstart = positions[3]
        if left and right: 
            if left[0] < right[0]:
                left = left[1:]
                lstart +=1
                changeColor(rstart,defaultColor)
            elif left[0] == right[0]:
                changeColor(lstart,defaultColor)
                changeColor(rstart,defaultColor)
                left = left[1:]
                lstart += 1
            else: 
                temp = vals[rstart]
                shiftRight(range(rstart, lstart, -1))
                vals[lstart] = temp
                updateScreen()

                right = right[1:]
                rstart += 1
                lstart += 1
                changeColor(lstart - 1, selectColor)
        elif left:
            changeColor(lstart, defaultColor)
            lstart += 1
            left = left[1:]
        elif right:
            changeColor(rstart, defaultColor)
            rstart += 1
            right = right[1:]
        
        if left or right:
            positions[0] = left
            positions[1] = right
            positions[2] = lstart
            positions[3] = rstart
            root.after(sortSpeed, lambda: mergeAnimation(False, positions, lstart - 1)) 
        else: 
            root.after(sortSpeed, lambda: mergeAnimation(True))

def mergeCombination(left, right): #another helper method for merge
    combined = []
    while left and right: 
        if left[0] <= right[0]:
            combined.append(left[0])
            left = left[1:]
        else:
            combined.append(right[0])
            right = right[1:]
    if left: 
        combined += left
    elif right: 
        combined += right
    return combined

#Merge Algo

def merge(list = None, newSort = True, start = 0, end = 0):
    global sorting 
    if sorting and newSort:
        return
    elif newSort:
        sorting = True
        buttonColor(merge,True)
        end = size
    list = vals if not list else list

    #Merge Algo
    length = len(list)
    if length == 1:
        return list
    middle = length // 2 if length % 2 == 0 else length // 2 + 1
    left = merge(list[: middle], False, start, middle)
    right = merge(list[middle:], False, start + middle, end)
    list = mergeCombination(left, right)
    mergeQueue.append([left, right, start, start + middle])

    if len(list) == len(vals):
        mergeAnimation()
    else: 
        return list

#2) HEAP SORT

def heap(index = None, maxHeap = [], newSort = True, step = 1): 
    global interrupted, sorting, vals
    if sorting and newSort:
        return
    elif newSort: 
        sorting = True
        buttonColor(heap, True)
        index = size - 1
        maxHeap = [-x for x in vals]
        heapify(maxHeap)
    changeColor(0, defaultColor) if not newSort else False
    if index == -1 or interrupted:
        interrupted = False
        sorting = False
        buttonColor(heap, False)
        return
    
    #Heap Algo

    if step == 1:
        changeColor(0, selectColor)
        root.after(sortSpeed, lambda: heap(index, maxHeap,False,2))
    else: 
        vals[index] = -heappop(maxHeap)
        vals[:index] = [-x for x in maxHeap]
        updateScreen()
        changeColor(index, selectColor)
        root.after(sortSpeed, lambda: heap(index-1,maxHeap,False,1))

        
#4) INSERTION SORT

def insertion(start = 1, iteration = 0, newSort = True, prev = False):
    global interrupted, sorting
    changeColor(prev, defaultColor) if type(prev) == int else None
    if sorting and newSort:
        return
    elif newSort:
        sorting = True
        buttonColor(insertion, True)
    if start == size or interrupted: #end conditions
        interrupted = False
        sorting = False
        buttonColor(insertion, False)
        return
    
    #Insertion Algo

    if iteration % 2 == 0:
        changeColor(start, selectColor)
        root.after(sortSpeed, lambda: insertion(start, iteration + 1, False))
    else:
        min = 1
        for i in range(start, 0, -1):
            if vals[i] < vals[i - 1]:
                swap(i, i - 1)
                min = i - 1
            else:
                min = i
                break
        clearRectangles(range(min, start + 1))
        for k in range(min, start + 1):
            drawRect(k , defaultColor)
        changeColor(min, selectColor)
        root.after(sortSpeed, lambda:insertion(start + 1, 0, False, min))



#5) SELECTION SORT

def selection(start = 0, newSort = True, iteration = 0, currMin = float('inf'), minIndex = None):
    global interrupted, sorting
    if sorting and newSort:
        return
    elif newSort:
        sorting = True
        buttonColor(selection, True)
    if start == size or interrupted: #end conditions
        changeColor(start - 1, defaultColor)
        interrupted = False
        sorting = False
        buttonColor(selection, False)
        return
    
    #Selection Algo

    if iteration % 2 == 0:
        changeColor(start - 1, defaultColor) if start != 0 else None
        for i in range(start, size):
            if vals[i] < currMin:
                currMin = vals[i]
                minIndex = i
        changeColor(minIndex, selectColor)
        root.after(sortSpeed, lambda: selection(start, False, iteration + 1, currMin, minIndex))
    else: 
        clearRectangles([minIndex, start])
        swap(start, minIndex)
        drawRect(start,selectColor)
        drawRect(minIndex,defaultColor)
        root.after(sortSpeed,lambda: selection(start + 1, False))

def swap(index1, index2):
	vals[index1], vals[index2] = vals[index2], vals[index1]

def changeColor(index, color):
    canvas.itemconfig(bars[index], fill=color, outline = color)

def drawRect(i, color):
    barWidth = (width * 0.9) / size
    startX = width * 0.05
    endY = height * 0.885

    x1 = startX + i * barWidth
    y1 = endY - (vals[i] / (size * 10)) * (.8 * height)
    x2 = x1 + barWidth
    bars[i] = canvas.create_rectangle(x1, y1, x2, endY, fill = color, outline = color, tag = 'rect')

def clearRectangles(list):
    if not list:
        canvas.delete('rect')
    else:
        for index in list:
            canvas.delete(bars[index])

def updateScreen():
    global bars
    clearRectangles(None) #clears all rec
    bars = [None] * size
    for i in range(size):
        drawRect(i, defaultColor)

def randomVals():
    global vals 
    random.seed(time.time())
    vals = [None] * size
    for i in range(size):
        vals[i] = random.randint(1, size * 10)
    updateScreen()

def changeSize(newSize):
    global size, interrupted
    interrupted = True if sorting else False
    size = int(newSize)
    randomVals()

def buttonColor(algorithm, pressed):
    index = functions.index(algorithm)
    buttons[index]['highlightbackground'] = 'beige' if pressed else 'white'

#speed methods
def slow():
    global sortSpeed
    sortSpeed = 300
    speedButton[0]['highlightbackground'] = 'beige'
    speedButton[1]['highlightbackground'] = 'white'
    speedButton[2]['highlightbackground'] = 'white'

def medium():
    global sortSpeed
    sortSpeed = 70
    speedButton[0]['highlightbackground'] = 'white'
    speedButton[1]['highlightbackground'] = 'beige'
    speedButton[2]['highlightbackground'] = 'white'

def fast():
    global sortSpeed
    sortSpeed = 1
    speedButton[0]['highlightbackground'] = 'white'
    speedButton[1]['highlightbackground'] = 'white'
    speedButton[2]['highlightbackground'] = 'beige'


#constants for buttons
sorts = ["Quick Sort", "Merge Sort", "Heap Sort", "Insertion Sort", "Selection Sort"]
functions = [quicksort, merge, heap, insertion, selection]
mode = ["Slow", "Medium", "Fast"]
speed = [slow, medium, fast]
buttons = []
speedButton = []

for i in range(len(sorts)): #create all the sorting buttons 
    buttons.append(tk.Button(canvas, text = sorts[i], command = functions[i]))
    buttons[i].place(relx = 0.005 * (i+1) + buttonWidth * i, rely = 0.005, relwidth=buttonWidth, relheight= buttonHeight)

inputSize = tk.Scale(canvas, from_ = 10, to = 500, tickinterval=90, orient = tk.HORIZONTAL, bg = '#ecc19c', command = changeSize)
inputSize.place(relx = 0.5 - buttonWidth * 4.5, rely = 1 - buttonHeight * 2.1, relwidth = buttonWidth * 6, relheight = buttonHeight * 2)
inputSize.set(size)

randomizer = tk.Button(canvas, text='Reset/Randomize', command = lambda: changeSize(size))
randomizer.place(relx=1-buttonWidth*1.1, rely=0.005,relwidth=buttonWidth, relheight=buttonHeight)

for i in range(3): #create speed buttons
    speedButton.append(tk.Button(canvas, text = mode[i], command = speed[i]))
    speedButton[i].place(relx = 0.5 + 1.75 * buttonWidth + buttonWidth * i, rely = 1 - buttonHeight * 1.55, relwidth = buttonWidth, relheight = buttonHeight)

randomVals()
slow()
root.mainloop()