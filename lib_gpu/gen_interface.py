import csv
import sys

(_, csv_file, output_prefix) = sys.argv
FUNCTION_TEMPLATE = '''NV_STATUS %(name)s(%(param_list)s) {
  static %(pointer_decl)s  = 0;
  if(!pointer) {pointer = (%(pointer_type)s)nvidia_handle->query(0x%(ID)s); }
  return (*pointer)(%(param_names)s);
}

'''

FUNCTION_DECLARATION_TEMPLATE = '''NVLIB_EXPORTED NV_STATUS %(name)s(%(param_list)s);

'''

with open(csv_file, 'rb') as file:
  output_file = '%s_gen.cpp' % (output_prefix)
  output_header = '%s_gen.h' % (output_prefix)
  with open(output_header, 'wb') as headerfile:
    with open(output_file, 'wb') as bodyfile:
      reader = csv.reader(file)
      comment = []
      for row in reader:
        if len(row) == 0 or len(row[0]) == 0:
          continue

        if row[0][0] == '#':
          comment_row = ", ".join(row)[1:]
          comment.append(' * ' + comment_row.strip())
          continue

        if len(row) < 2:
          continue

        ID = row[0]
        function_name = 'NVIDIA_RAW_%s' % row[1]
        params = row[2:]
        param_types = []
        param_names = []
        for p in params:
          parts = p.split(' ')
          param_types.append(' '.join(parts[0:-1]))
          param_names.append(parts[-1])

        param_type_str = ', '.join(param_types)
        param_name_str = ', '.join(param_names)
        param_list_str = ', '.join(params)
        pointer_type = 'NV_STATUS (*)(%s)' % param_type_str
        pointer_decl = 'NV_STATUS (*pointer)(%s)' % param_type_str

        template_args = {
          'name': function_name,
          'ID': ID,
          'param_list': param_list_str,
          'param_names': param_name_str,
          'pointer_type': pointer_type,
          'pointer_decl': pointer_decl
        }

        bodyfile.write(FUNCTION_TEMPLATE % template_args)
        if len(comment) > 0:
          comment_str = '/**\n' + '\n'.join(comment) + '\n */\n'
          headerfile.write(comment_str)
          comment = []
        headerfile.write(FUNCTION_DECLARATION_TEMPLATE % template_args)

