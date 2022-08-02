pytnon -m venv venv

windows: ./venv/Scripts/activate
linux: source ./venv/bin/activate

pip install -r requirements.txt

create file .env and write there:
```
TOKEN=<your discord token>

```
save and quit

python main.py