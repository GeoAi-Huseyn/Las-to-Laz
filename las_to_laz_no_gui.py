import tkinter as tk
from tkinter import filedialog
import subprocess
import os


def input_data(title="Faylları seçin", filetypes=None):
    try:
        if filetypes is None:
            filetypes = [("All Files", "*.*")]

        root = tk.Tk()
        root.withdraw()

        file_paths = filedialog.askopenfilenames(
            title=title,
            filetypes=filetypes
        )

        if not file_paths:
            raise ValueError("Heç bir fayl seçilmədi.")

        return file_paths

    except ValueError as ve:
        print(ve)
    except Exception as e:
        print("Xəta baş verdi:", e)


def output_data(title="Papka seçin"):
    try:
        root = tk.Tk()
        root.withdraw()

        folder_path = filedialog.askdirectory(title=title)

        if not folder_path:
            raise ValueError("Heç bir papka seçilmədi.")
        
        return folder_path
    
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print("Xəta baş verdi:", e)


def select_laszip():
    """laszip.exe faylını seçmək üçün"""
    try:
        print("laszip.exe faylını seçin")
        root = tk.Tk()
        root.withdraw()
        
        file_path = filedialog.askopenfilename(
            title="laszip.exe faylını seçin",
            filetypes=[("Executable Files", "*.exe"), ("All Files", "*.*")]
        )
        
        if not file_path:
            raise ValueError("laszip.exe seçilmədi.")
        
        return file_path
                    
    except ValueError as ve:
        print(ve)
        return None
    except Exception as e:
        print("Xəta baş verdi:", e)
        return None


def progress_las_to_laz(input_files, output_folder, laszip_path):
    """LAS fayllarını LAZ formatına çevirir (mövcud faylların üzərinə yazır)"""
    try:
        if not laszip_path or not os.path.exists(laszip_path):
            print("Xəta: laszip.exe tapılmadı!")
            return 0, len(input_files)
        
        successful = 0
        failed = 0
        
        for input_file in input_files:
            try:
                print(f"\nÇevrilir: {os.path.basename(input_file)}")
                
                # Çıxış faylının adını təyin et
                output_filename = os.path.basename(input_file).replace('.las', '.laz')
                output_file = os.path.join(output_folder, output_filename)
                
                # Əgər fayl mövcuddursa, xəbərdarlıq ver
                if os.path.exists(output_file):
                    print(f"⚠ Diqqət: {output_filename} mövcuddur, üzərinə yazılacaq...")
                
                # CMD komandası (-odir və -olaz istifadə edək)
                command = [
                    laszip_path,
                    '-i', input_file,
                    '-o', output_file,
                    '-olaz'  # LAZ formatında çıxarış
                ]
                
                print(f"Komanda: {' '.join(command)}")
                
                # Prosesi işə sal
                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
                
                stdout, stderr = process.communicate()
                
                if process.returncode == 0:
                    print(f"✓ Uğurlu: {output_filename}")
                    successful += 1
                else:
                    print(f"✗ Xəta: {output_filename}")
                    if stderr:
                        print(f"  Xəta mesajı: {stderr}")
                    if stdout:
                        print(f"  Çıxış: {stdout}")
                    failed += 1
                    
            except Exception as e:
                print(f"✗ Xəta ({os.path.basename(input_file)}): {e}")
                failed += 1
        
        # Yekun nəticə
        print("\n" + "="*50)
        print(f"ÜMUMİ NƏTİCƏ:")
        print(f"  Uğurlu: {successful}")
        print(f"  Uğursuz: {failed}")
        print(f"  Cəmi: {len(input_files)}")
        print("="*50)
        
        return successful, failed
        
    except Exception as e:
        print(f"Ümumi xəta: {e}")
        return 0, len(input_files)


# ƏSAS PROQRAM
if __name__ == "__main__":
    print("="*50)
    print("LAS to LAZ Converter")
    print("="*50)
    
    # laszip.exe seç
    laszip_path = select_laszip()
    
    if not laszip_path:
        print("Proqram dayandırıldı: laszip.exe seçilmədi")
        input("\nProqramı bağlamaq üçün Enter basın...")
        exit()
    
    # Input faylları seç
    print("\nInput LAS fayllarını seçin...")
    input_files = input_data(filetypes=[("LAS Files", "*.las"), ("All Files", "*.*")])
    
    if not input_files:
        print("Proqram dayandırıldı: Fayl seçilmədi")
        input("\nProqramı bağlamaq üçün Enter basın...")
        exit()
    
    # Output qovluğu seç
    print("\nOutput qovluğunu seçin...")
    output_folder = output_data()
    
    if not output_folder:
        print("Proqram dayandırıldı: Qovluq seçilmədi")
        input("\nProqramı bağlamaq üçün Enter basın...")
        exit()
    
    # Çevirmə prosesini başlat
    print(f"\n{len(input_files)} fayl çevriləcək...")
    progress_las_to_laz(input_files, output_folder, laszip_path)
    
    input("\nProqramı bağlamaq üçün Enter basın...")