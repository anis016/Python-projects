
* Sign in to Oxford dictionary API - [Oxford Dictionaries](https://developer.oxforddictionaries.com/) and 
get the `app_id` and `app_key`
* Store the `app_id` and `app_key` in a text file like below.
```bash
$ cat oxford_api_key
app_id = <your_app_id>
app_key = <your_app_keys>
```
* Run the `secure.py` to encrypt the api key file
* Run the `definition.py <word>` to show the word definitions
```python
python definition.py Example
 ```
* Output
```python
Word: Example

English definition: a thing characteristic of its kind or illustrating a general rule
English definition: a person or thing regarded in terms of their fitness to be imitated
English definition: be illustrated or exemplified
```

TODO:
1. Check if the word is correct or not