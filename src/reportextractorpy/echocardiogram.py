# from collections import UserDict
#
#
# # Creating a Dictionary where
# # deletion is not allowed
# class MyDict(UserDict):
#
#     def __init__(self):
#         # read json file
#
#     # Function to stop deletion from dictionary
#     def __del__(self):
#         raise RuntimeError("Deletion not allowed")
#
#     # Function to stop pop from dictionary
#     def pop(self, s=None):
#         raise RuntimeError("Deletion not allowed")
#
#     # Function to stop popitem from Dictionary
#     def popitem(self, s=None):
#         raise RuntimeError("Deletion not allowed")
#
#
# # Driver's code
# d = MyDict({'a': 1,
#             'b': 2,
#             'c': 3})
#
# print("Original Dictionary")
# print(d)
#
# d.pop(1)