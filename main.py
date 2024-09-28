import flet as ft
import base64
import marshal
import os
import asyncio
import zlib
import random
import string
import hashlib
from tqdm import tqdm

def encrypt_python_file(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"الملف غير موجود: {file_path}")
        
        if not file_path.lower().endswith('.py'):
            raise ValueError("الملف المحدد ليس ملف بايثون (.py)")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        print("تم قراءة الملف بنجاح")
        
        wrapped_code = f"exec('''{source_code}''')"
        print("تم تغليف الكود")
        
        code_object = compile(wrapped_code, '<string>', 'exec')
        print("تم تجميع الكود")
        
        marshaled_data = marshal.dumps(code_object)
        print("تم ترميز الكود")
        
        encoded_data = base64.b64encode(marshaled_data).decode('utf-8')
        print("تم تشفير الكود")
        
        decryption_code = f'''
import base64
import marshal

def decrypt_and_run(encrypted_code):
    try:
        decoded_data = base64.b64decode(encrypted_code)
        code_object = marshal.loads(decoded_data)
        exec(code_object)
    except Exception as e:
        print(f"خطأ أثناء فك التشفير أو التنفيذ: {{str(e)}}")

encrypted_code = "{encoded_data}"

decrypt_and_run(encrypted_code)
'''
        
        print("تم إنشاء كود فك التشفير")
        return decryption_code
    
    except FileNotFoundError as fnf_error:
        print(f"خطأ في العثور على الملف: {str(fnf_error)}")
        raise
    except ValueError as v_error:
        print(f"خطأ في التحقق من الملف: {str(v_error)}")
        raise
    except Exception as general_error:
        print(f"خطأ غير متوقع أثناء تشفير الملف: {str(general_error)}")
        raise

def encrypt_easy(source_code):
    encoded = base64.b64encode(source_code.encode()).decode()
    return f'''
import base64

exec(base64.b64decode("{encoded}").decode())
'''

def encrypt_medium(source_code, layers):
    code = source_code
    for _ in range(layers):
        code_object = compile(code, '<string>', 'exec')
        marshaled_data = marshal.dumps(code_object)
        code = f'import marshal\nexec(marshal.loads({marshaled_data}))'
    
    encoded_data = base64.b64encode(code.encode()).decode('utf-8')
    return f'''
import base64
exec(base64.b64decode("{encoded_data}").decode())
'''

def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def encrypt_hard(source_code, layers):
    # تشفير الكود الأصلي
    code_object = compile(source_code, '<string>', 'exec')
    marshaled_code = marshal.dumps(code_object)
    compressed_code = zlib.compress(marshaled_code)
    encoded_code = base64.b85encode(compressed_code)
    
    keys = []
    for _ in range(layers):
        key = random.randint(1, 255)
        encoded_code = bytes(b ^ key for b in encoded_code)
        keys.append(key)
    
    # إنشاء كود فك التشفير
    decryption_code = f'''
import base64, marshal, zlib, random, time, sys, os
from tqdm import tqdm

def xor_decrypt(data, key):
    return bytes(b ^ key for b in data)

encrypted_data = {encoded_code}
keys = {keys}

for key in tqdm(reversed(keys), desc="جاري فك تشفير الطبقات", bar_format="{{l_bar}}{{bar}}", ncols=50):
    encrypted_data = xor_decrypt(encrypted_data, key)
    time.sleep(0.01)

compressed_code = base64.b85decode(encrypted_data)
marshaled_code = zlib.decompress(compressed_code)
code_object = marshal.loads(marshaled_code)
exec(code_object)
'''
    
    # تشفير كود فك التشفير
    compiled_decryption_code = compile(decryption_code, '<string>', 'exec')
    marshaled_decryption_code = marshal.dumps(compiled_decryption_code)
    compressed_decryption_code = zlib.compress(marshaled_decryption_code)
    final_encrypted_code = base64.b85encode(compressed_decryption_code)
    
    # إنشاء الملف النهائي مع تشويش إضافي
    decode_func = random_string(10)
    decompress_func = random_string(10)
    loads_func = random_string(10)
    exec_func = random_string(10)
    
    final_code = f'''
# أداة تشفير CODESF3
# تيليجرام: @c_ega
# جميع الحقوق محفوظة.

import base64, zlib, marshal, random, time, sys, os
from tqdm import tqdm

class CodeLoader:
    @staticmethod
    def {decode_func}(x):
        return base64.b85decode(x)

    @staticmethod
    def {decompress_func}(x):
        return zlib.decompress(x)

    @staticmethod
    def {loads_func}(x):
        return marshal.loads(x)

encrypted_code = {final_encrypted_code}

def {exec_func}():
    decrypted = CodeLoader.{decode_func}(encrypted_code)
    decompressed = CodeLoader.{decompress_func}(decrypted)
    code_object = CodeLoader.{loads_func}(decompressed)
    exec(code_object)

if __name__ == "__main__":
    {exec_func}()

{chr(10).join([f"# {random_string(50)}" for _ in range(100)])}
'''
    return final_code

def main(page: ft.Page):
    page.title = "CODESF3 - تشفير ملفات بايثون"
    page.window_width = 400  # زيادة عرض النافذة
    page.window_height = 800  # زيادة ارتفاع النافذة
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.colors.BLACK

    async def show_snack_bar(message: str, color: str):
        snack_bar = ft.SnackBar(
            content=ft.Text(message, color=color),
            bgcolor=ft.colors.BLUE_GREY_900,
        )
        page.snack_bar = snack_bar
        snack_bar.open = True
        page.update()
        await asyncio.sleep(1.5)
        snack_bar.open = False
        page.update()

    confirmation_text = ft.Text("", color=ft.colors.WHITE, size=18, text_align="center")
    confirmation_container = ft.Container(
        content=confirmation_text,
        alignment=ft.alignment.center,
        width=400,
        height=50,
        bgcolor=ft.colors.BLUE_GREY_900,
        border_radius=10,
        visible=False
    )

    async def show_confirmation(message: str):
        confirmation_text.value = message
        confirmation_container.visible = True
        page.update()
        await asyncio.sleep(1.5)
        confirmation_container.visible = False
        page.update()

    encryption_level = ft.Dropdown(
        width=350,
        options=[
            ft.dropdown.Option("سهل"),
            ft.dropdown.Option("متوسط"),
            ft.dropdown.Option("صعب"),
        ],
        value="متوسط",
        label="مستوى التشفير",
    )

    layers_text = ft.Text("عدد الطبقات: 50", color=ft.colors.WHITE)
    
    layers_slider = ft.Slider(
        min=1,
        max=100,
        value=50,
        label="{value}",
        width=350,
    )

    def update_layers_text(e):
        layers_text.value = f"عدد الطبقات: {int(e.control.value)}"
        page.update()

    layers_slider.on_change = update_layers_text

    async def encrypt_file_async(e):
        try:
            if not selected_file.value:
                raise ValueError("الرجاء اختيار ملف بايثون (.py)")
            
            if not selected_file.value.lower().endswith('.py'):
                raise ValueError("الملف المحدد ليس ملف بايثون (.py)")
            
            with open(selected_file.value, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            layers = int(layers_slider.value)
            
            if encryption_level.value == "سهل":
                encrypted = encrypt_easy(source_code)
            elif encryption_level.value == "متوسط":
                encrypted = encrypt_medium(source_code, layers)
            else:
                encrypted = encrypt_hard(source_code, layers)
            
            output_field.value = encrypted
            save_button.disabled = False
            page.update()
            await show_confirmation("تم التشفير بنجاح")
        except Exception as ex:
            error_message = f"خطأ: {str(ex)}"
            output_field.value = error_message
            page.update()
            await show_confirmation("لم يتم تشفير الملف")

    def encrypt_file(e):
        asyncio.run(encrypt_file_async(e))

    def pick_file(e):
        pick_file_dialog.pick_files(allow_multiple=False, allowed_extensions=['py'])

    def save_file(e):
        save_file_dialog.save_file(file_name="encrypted_file.py", allowed_extensions=['py'])

    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            selected_file.value = e.files[0].path
            file_path.value = e.files[0].name
            page.update()

    def on_file_saved(e: ft.FilePickerResultEvent):
        if e.path:
            try:
                with open(e.path, 'w', encoding='utf-8') as f:
                    f.write(output_field.value)
                output_field.value = f"تم حفظ الملف المشفر في: {e.path}"
            except Exception as ex:
                output_field.value = f"خطأ أثناء حفظ الملف: {str(ex)}"
        else:
            output_field.value = "تم إلغاء عملية الحفظ"
        page.update()

    def clear_fields(e):
        selected_file.value = ""
        file_path.value = ""
        output_field.value = ""
        save_button.disabled = True
        page.update()

    def show_social_links(e):
        social_dialog.open = True
        page.update()

    title = ft.Text(
        "CODESF3",
        size=32,
        weight="bold",
        color=ft.colors.BLUE_200,
        text_align="center"
    )
    
    subtitle = ft.Text(
        "تشفير ملفات بايثون",
        size=18,
        color=ft.colors.BLUE_100,
        text_align="center"
    )
    
    selected_file = ft.Text()
    file_path = ft.Text("لم يتم اختيار ملف", color=ft.colors.GREY_400)
    
    pick_file_dialog = ft.FilePicker(on_result=on_file_picked)
    save_file_dialog = ft.FilePicker(on_result=on_file_saved)
    page.overlay.extend([pick_file_dialog, save_file_dialog])
    
    pick_button = ft.ElevatedButton(
        "اختيار ملف",
        icon=ft.icons.UPLOAD_FILE,
        on_click=pick_file,
        width=350,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.BLUE_700,
            elevation=5,
            shape=ft.RoundedRectangleBorder(radius=20),
        ),
    )
    
    output_field = ft.TextField(
        label="النص المشفر",
        multiline=True,
        min_lines=5,
        max_lines=8,
        width=350,
        read_only=True,
        border_color=ft.colors.GREEN_400,
        text_size=16,
    )

    encrypt_button = ft.ElevatedButton(
        content=ft.Row([ft.Icon(ft.icons.LOCK), ft.Text("تشفير الملف")]),
        on_click=encrypt_file,
        width=165,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.GREEN_700,
            elevation=5,
            shape=ft.RoundedRectangleBorder(radius=20),
        ),
    )

    save_button = ft.ElevatedButton(
        content=ft.Row([ft.Icon(ft.icons.SAVE), ft.Text("حفظ الملف المشفر")]),
        on_click=save_file,
        width=300,
        disabled=True,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.ORANGE_700,
            elevation=5,
            shape=ft.RoundedRectangleBorder(radius=20),
        ),
    )

    menu_button = ft.IconButton(
        icon=ft.icons.MORE_VERT,
        icon_color=ft.colors.BLUE_400,
        tooltip="روابط التواصل الاجتماعي",
        on_click=show_social_links,
    )

    social_dialog = ft.AlertDialog(
        title=ft.Text("روابط التواصل الاجتماعي"),
        content=ft.Column([
            ft.TextButton(
                content=ft.Row([
                    ft.Icon(ft.icons.TELEGRAM, color=ft.colors.BLUE_400),
                    ft.Text("تليجرام: @c_ega")
                ]),
                on_click=lambda _: page.launch_url("https://t.me/c_ega")
            ),
            ft.TextButton(
                content=ft.Row([
                    ft.Icon(ft.icons.TIKTOK, color=ft.colors.PINK_400),
                    ft.Text("تيك توك: @sf3")
                ]),
                on_click=lambda _: page.launch_url("https://www.tiktok.com/@sf3")
            ),
        ]),
        actions=[
            ft.TextButton("إغلاق", on_click=lambda _: setattr(social_dialog, 'open', False))
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    save_and_menu_row = ft.Row(
        [save_button, menu_button],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    page.dialog = social_dialog

    clear_button = ft.IconButton(
        icon=ft.icons.CLEAR,
        icon_color=ft.colors.RED_400,
        tooltip="مسح الحقول",
        on_click=clear_fields,
    )

    # إنشاء محتوى الصفحة
    content = ft.Column(
        [
            ft.Container(content=title, margin=ft.margin.only(bottom=5, top=20)),
            ft.Container(content=subtitle, margin=ft.margin.only(bottom=20)),
            pick_button,
            ft.Container(content=file_path, margin=ft.margin.only(top=10, bottom=10)),
            encryption_level,
            ft.Container(height=10),
            layers_text,
            layers_slider,
            ft.Container(height=10),
            encrypt_button,
            ft.Container(height=10),
            confirmation_container,
            ft.Container(height=10),
            ft.Container(
                content=output_field,
                border_radius=10,
                padding=10,
                bgcolor=ft.colors.BLUE_GREY_900,
            ),
            ft.Container(height=10),
            save_and_menu_row,
            ft.Container(height=10),
            clear_button,
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True,  # يسمح للمحتوى بالتمدد ليملأ المساحة المتاحة
    )

    # إنشاء حاوية تحتوي على المحتوى
    main_container = ft.Container(
        content=content,
        expand=True,  # يسمح للحاوية بالتمدد لتملأ المساحة المتاحة
        padding=20,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.colors.BLACK, ft.colors.BLUE_900],
        ),
    )

    # إضافة الحاوية إلى الصفحة
    page.add(main_container)

    # تحديث الصفحة عند تغيير حجم النافذة
    def page_resize(e):
        main_container.height = page.window_height
        main_container.width = page.window_width
        page.update()

    page.on_resize = page_resize

ft.app(target=main)
