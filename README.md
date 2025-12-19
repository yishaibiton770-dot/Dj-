# DJ AI scaffold

זהו מימוש התחלתי של ממשק "די.ג'יי AI" שמדגים איך אפשר:

- לסרוק ספריית שירים מקומית ולבנות מטא-דטה בסיסי.
- להריץ "אנליזה" דטרמיניסטית (BPM, סולם, פרופיל אנרגיה, beat grid, חלוקת מקטעים).
- להציע תכנית מעבר בין שני שירים (mix in/out, כוונון קצב, צעד־אחר־צעד של אפקטים).
- לבנות תכנית ביטים/רמיקס ולשמור את שני סוגי התכניות כקובצי JSON קריאים.

> **הערה**: זהו אב-טיפוס קליל ללא DSP אמיתי. הערכים נגזרים מתוכן הקובץ כך שיהיו עקביים, אבל לא ממדלים אודיו אמיתי.

## הרצה מהירה

```bash
python -m djai.cli ./demo_library ./outputs
```

הפקודה:
1. סורקת את `./demo_library`.
2. מנתחת כל שיר ומעדכנת את הספרייה.
3. בונה רמיקס בסיסי לכל שיר.
4. אם יש לפחות שני שירים – בונה גם תכנית מעבר בין השניים הראשונים.
5. שומרת את כל הפלט בתיקיית `./outputs`.

## יצירת ספריית דמו

ניתן ליצור ספרייה בסיסית עם קבצי placeholder:

```python
from pathlib import Path
from djai.library import SongLibrary

library = SongLibrary.demo_library(Path("demo_library"))
library.save(Path("outputs/library.json"))
```

## מבנה הקוד

- `djai/library.py` – מודל נתונים של שיר וספרייה + סריקה/שמירה.
- `djai/audio_analysis.py` – אנליזה דטרמיניסטית: BPM, סולם, פרופיל אנרגיה, beat grid ומקטעים.
- `djai/transition_engine.py` – חישוב תכנית מעבר בסיסית בין שני שירים.
- `djai/remix_builder.py` – בניית דפוס תופים ו-overlay על beat grid.
- `djai/render_engine.py` – כתיבת תכניות מעבר/רמיקס כ-JSON.
- `djai/cli.py` – CLI שמחבר את כל השלבים מקצה לקצה.

## בדיקות

יש בדיקת אינטגרציה קטנה שמוודאת שה-flow המלא רץ עם ספריית דמו:

```bash
python -m unittest discover
```
