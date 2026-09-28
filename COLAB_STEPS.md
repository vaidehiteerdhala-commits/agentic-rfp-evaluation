# Google Colab Verification

```python
from google.colab import files
files.upload()
```
```bash
!unzip -q rfp_agentic_project_v2.zip -d /content
%cd /content/rfp_agentic_project_v2
!pip install -q -r requirements.txt
!python db/seed_db.py
!python run_demo.py
!python -m pytest -q
```
Do not paste an API key into notebook cells.
