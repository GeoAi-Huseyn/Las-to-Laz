import tkinter as tk
from tkinter import filedialog
import subprocess
import os
import ctypes



def get_short_path_name(path):
    """Windows qısa yolunu (8.3 formatı) əldə edir - Unicode problemlərini həll etmək üçün"""
    if not os.path.exists(path):
        return path
    buffer_size = 256
    buffer = ctypes.create_unicode_buffer(buffer_size)
    get_short_path_name_w = ctypes.windll.kernel32.GetShortPathNameW
    res = get_short_path_name_w(path, buffer, buffer_size)
    if res > buffer_size:
        buffer = ctypes.create_unicode_buffer(res)
        get_short_path_name_w(path, buffer, res)
    return buffer.value


def input_data(title="Faylları seçin", filetypes=None):
    try:
        if filetypes is None:
            filetypes = [("All Files", "*.*")]




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
                output_filename = os.path.splitext(os.path.basename(input_file))[0] + '.laz'
                output_file = os.path.join(output_folder, output_filename)
                
                # Əgər fayl mövcuddursa, xəbərdarlıq ver
                if os.path.exists(output_file):
                    print(f"⚠ Diqqət: {output_filename} mövcuddur, üzərinə yazılacaq...")
                
                # Pathları sistem formatına uyğunlaşdır (Windows üçün backslash)
                # Diqqət: 'İ' kimi hərflər laszip-də problem yaradır, ona görə ShortPath (8.3) istifadə edirik
                input_file_short = get_short_path_name(input_file)
                laszip_path_short = get_short_path_name(laszip_path)

                # Pathları sistem formatına uyğunlaşdır (Windows üçün backslash)
                input_dir = os.path.dirname(input_file)
                temp_input_name = "temp_safe_input.las"
                temp_input_full_path = os.path.join(input_dir, temp_input_name)
                
                # Əgər müvəqqəti fayl adı artıq mövcuddursa, onu silək (təhlükəsizlik üçün)
                if os.path.exists(temp_input_full_path):
                    try:
                        os.remove(temp_input_full_path)
                    except:
                        pass # Silə bilməsək davam edirik, rename xəta verəcək onsuz
                
                # Faylı müvəqqəti adla rename edirik (Unicode problemlərindən qaçmaq üçün)
                renamed_succesfully = False
                try:
                    os.rename(input_file, temp_input_full_path)
                    renamed_succesfully = True
                    print(f"  Fayl müvəqqəti adlandırıldı: {temp_input_name}")
                except Exception as e:
                    print(f"  Rename xətası: {e}")
                    # Rename alınmadısa, olduğu kimi davam etməyə çalışırıq (amma yəqin ki alınmayacaq)
                    temp_input_full_path = input_file

                # Output üçün müvəqqəti sadə ad
                temp_output_filename = "temp_safe_output.laz"
                temp_output_path = os.path.join(output_folder, temp_output_filename)
                
                # laszip path-ını da qısa yola çevir (əgər path-da boşluq və s. varsa)
                laszip_path_cmd = get_short_path_name(laszip_path)

                # CMD komandası
                command = [
                    laszip_path_cmd,
                    '-i', temp_input_full_path,
                    '-o', temp_output_path,
                    '-olaz'
                ]
                
                # Debug üçün komandanı çap et
                print(f"Komanda: {command}")
                
                # Prosesi işə sal
                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
                
                stdout, stderr = process.communicate()
                
                # Orijinal fayl adını mütləq bərpa edirik!
                if renamed_succesfully:
                    try:
                        os.rename(temp_input_full_path, input_file)
                        print(f"  Orijinal fayl adı bərpa olundu.")
                    except Exception as e:
                        print(f"!!! KRİTİK XƏTA: Fayl adını bərpa etmək olmadı: {e}")
                        print(f"Fayl indi buradadır: {temp_input_full_path}")

                if process.returncode == 0:
                    # Uğurlu bitibsə, output faylının adını düzəlt
                    final_output_path = os.path.join(output_folder, output_filename)
                    
                    if os.path.exists(final_output_path):
                        try:
                            os.remove(final_output_path) # Köhnəsi varsa sil
                        except:
                            pass
                    
                    if os.path.exists(temp_output_path):
                        os.rename(temp_output_path, final_output_path)
                        print(f"✓ Uğurlu: {output_filename}")
                        successful += 1
                    else:
                        print(f"✗ Xəta: Müvəqqəti çıxış faylı yaranmadı")
                        if stderr: print(f"  Stderr: {stderr}")
                        if stdout: print(f"  Stdout: {stdout}")
                        failed += 1
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
    
    # Tkinter root pəncərəsini bir dəfə yaraduruq
    root = tk.Tk()
    root.withdraw()
    
    # laszip.exe seç
    laszip_path = select_laszip()
    
    if not laszip_path:
        print("Proqram dayandırıldı: laszip.exe seçilmədi")
        input("\nProqramı bağlamaq üçün Enter basın...")
        exit()
    
    # Input faylları seç
    print("\nInput LAS fayllarını seçin...")
    input_files = input_data(title="LAS fayllarını seçin", filetypes=[("LAS Files", "*.las"), ("All Files", "*.*")])
    
    if not input_files:
        print("Proqram dayandırıldı: Fayl seçilmədi")
        input("\nProqramı bağlamaq üçün Enter basın...")
        exit()
    
    # Output qovluğu seç
    print("\nOutput qovluğunu seçin...")
    output_folder = output_data(title="Fayl hara yazılacaq seçin")
    
    if not output_folder:
        print("Proqram dayandırıldı: Qovluq seçilmədi")
        input("\nProqramı bağlamaq üçün Enter basın...")
        exit()
    
    # Çevirmə prosesini başlat
    print(f"\n{len(input_files)} fayl çevriləcək...")
    progress_las_to_laz(input_files, output_folder, laszip_path)
    
    input("\nProqramı bağlamaq üçün Enter basın...")