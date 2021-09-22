# Totally scuffed python script to generate a SUMMARY.md file with groups
import os

# Run from docs

def gen_gitbook_group(startpath):
    output = ""
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)

        # Expect a README.md in each folder
        if not os.path.basename(root) == "":
            output = output + ('{}* [{}]({})\n'.format(indent, os.path.basename(root), (startpath + os.path.basename(root) + "/README.md")))

        subindent = ' ' * 4 * (level + 1)

        for f in files:
            if not f == "README.md" and os.path.splitext(f)[1] == '.md':
                output = output + ('{}* [{}]({})\n'.format(subindent, os.path.splitext(f)[0], startpath + os.path.basename(root) + '/' + f))

    return output

summary = """
# Table of contents

* [Description](README.md)

## Knowledge Base

"""

summary = summary + gen_gitbook_group('knowledge-base/')

summary = summary + """

## Code Base

"""

summary = summary + gen_gitbook_group('code-base/')

summary_file = open('SUMMARY.md', 'w+')
summary_file.write(summary)
summary_file.close()
