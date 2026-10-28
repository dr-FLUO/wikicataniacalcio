import os
import shutil

src_dir = 'content/assets/img'
dst_dir = 'content/assets/images'

conflicts = []
to_copy = []

for root, dirs, files in os.walk(src_dir):
    rel_path = os.path.relpath(root, src_dir)
    target_subdir = os.path.join(dst_dir, rel_path) if rel_path != '.' else dst_dir
    for f in files:
        s_file = os.path.join(root, f)
        d_file = os.path.join(target_subdir, f)
        to_copy.append((s_file, d_file))
        if os.path.exists(d_file):
            conflicts.append((s_file, d_file))

print(f"Total files to move/copy: {len(to_copy)}")
print(f"Total conflicts: {len(conflicts)}")
for s, d in conflicts:
    print(f"Conflict: {s} -> {d}")
