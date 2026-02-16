# LAS to LAZ Converter (laszip + Tkinter)

Bu layihə **.las** fayllarını **.laz** formatına çevirmək üçün sadə bir **Python** skriptidir. Skript **Tkinter** pəncərələri ilə:
- `laszip.exe` faylını seçməyə,
- çevriləcək `.las` fayllarını toplu şəkildə seçməyə,
- çıxış qovluğunu seçməyə imkan verir.

Çevirmə prosesi `laszip.exe` vasitəsilə `subprocess` ilə icra olunur və konsolda uğurlu/uğursuz nəticələr göstərilir.

---

## Xüsusiyyətlər
- ✅ GUI (file picker) ilə **laszip.exe** seçimi
- ✅ Birdən çox **LAS** faylını eyni anda seçib çevirmə
- ✅ Output qovluğu seçimi
- ✅ Mövcud `.laz` faylı varsa xəbərdarlıq edib **üzərinə yazır**
- ✅ Konsolda detallı nəticə (uğurlu/uğursuz say)

---

## Tələblər
- Windows (çünki `laszip.exe` istifadə olunur)
- Python 3.8+ (tövsiyə)
- `laszip.exe` (LAStools / LASzip)

> Qeyd: Skript əlavə Python paketləri tələb etmir (`tkinter` standart kitabxanadır).

---
