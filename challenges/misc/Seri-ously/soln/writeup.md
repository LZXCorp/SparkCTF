# Deserialization challenge writeup

## Context of challenge:
The python source code creates an object which is serialized and sent. 

This is revealed as a bytestream.

## Solution Steps:

To view the actual data, it has to be deserialised. The pickle module in python is used for this. Example code: 

```python
import pickle
print(pickle.loads(data))
```

This is what looks like after it is deserialised

```python
{'User1': {'Status': 'Running', 'User': 'Jack'}, 'User2': {'Status': 'Red', 'User': 'Her', 'Access': 'ERROR', 'Item': 'Ring'}, 'User3': {'Status': 'Stopped', 'User': 'Tom', 'Access': False, 'Level': False}, 'User4': {'Status': 'Green'}, 'User5': {'Status': 'Enabled', 'User': 'Tom', 'Level': '3000'}, 'User6': {'Status': 'Unknown', 'User': 'ERROR', 'Access': 'ERROR', 'Level': 'ERROR'}}
```

To obtain the flag, the content of the object has to be modified. 
The vulnerable attribute is `ACCESS`, on `User3`. 

By changing it to `True`, serializing using pickle again and sending it back, the flag will be revealed. The python code only checks for the existence of `user3['ACCESS'] == TRUE`. It is possible to only submit that 1 attribute to obtain the flag.
```python
user3 = {'Status' : 'Stopped', 'User' : 'Tom', 
'Access' : True, 'Level': False}
```
(Note that this still has to be nested within the dictionary.)

From there, paste the serialized data into the python user input field and the flag will be revealed. 

## Answers

This is the minimum input required to obtain the flag

```python
b'\x80\x04\x95\x19\x00\x00\x00\x00\x00\x00\x00}\x94\x8c\x05User3\x94}\x94\x8c\x06Access\x94\x88ss.'
```

Sample python code to generate minimum solution:

```python
import pickle

user3 = {'Access' : True}
db = {}
db['User3'] = user3

x = pickle.dumps(db)
print(x)
```
