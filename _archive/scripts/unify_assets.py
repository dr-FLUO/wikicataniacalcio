import os
import shutil

src_base = os.path.abspath('content/assets/img')
dst_base = os.path.abspath('content/assets/images')

if not os.path.exists(src_base):
    print("Source directory does not exist:", src_base)
    exit(0)

print(f"Moving from {src_base} to {dst_base}...")

moved_count = 0
for item in os.listdir(src_base):
    s = os.path.join(src_base, item)
    d = os.path.join(dst_base, item)
    if os.path.isdir(s):
        if os.path.exists(d):
            # merge directory
            for sub_root, sub_dirs, sub_files in os.walk(s):
                rel = os.path.relpath(sub_root, s)
                target_sub = os.path.join(d, rel)
                os.makedirs(target_sub, exist_ok=True)
                for f in sub_files:
                    f_src = os.path.join(sub_root, f)
                    f_dst = os.path.join(target_sub, f)
                    shutil.move(f_src, f_dst)
                    moved_count += 1
            shutil.rmtree(s)
        else:
            shutil.move(s, d)
            # count files
            for _, _, files in os.walk(d):
                moved_count += len(files)
    else:
        shutil.move(s, d)
        moved_count += 1

# Check if empty and remove
if os.path.exists(src_base):
    try:
        os.rmdir(src_base)
        print(f"Removed empty source directory: {src_base}")
    except Exception as e:
        print(f"Notice: {e}")

print(f"Successfully moved {moved_count} files into {dst_base}.")
