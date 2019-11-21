import os
import subprocess
from django.conf import settings
from users.models import Member


def generate_membership_card(ids):
    library_name = settings.LIBRARY_INFORMATION.get('NAME', 'Library Name')
    background_pic_path = os.path.join(settings.BASE_DIR,
                                       'reports/templates/reports/latex/membership_card/background.jpg')
    single_card_template_path = os.path.join(settings.BASE_DIR,
                                             'reports/templates/reports/latex/membership_card/single_card_template.tex')
    membership_card_template_path = os.path.join(settings.BASE_DIR,
                                                 'reports/templates/reports/latex/membership_card/template.tex')
    temp_file_path = os.path.join(settings.BASE_DIR,
                                  'reports/templates/reports/latex/generated_reports/temp.tmp')
    members_card_path = os.path.join(settings.BASE_DIR,
                                     'reports/templates/reports/latex/generated_reports/members_card.tex')
    members_card_pdf_path = os.path.join(settings.BASE_DIR,
                                         'reports/templates/reports/latex/generated_reports/members_card.pdf')
    output_dir = os.path.join(settings.BASE_DIR, 'reports/templates/reports/latex/generated_reports/')
    ith_card = 1

    with open(single_card_template_path, 'r') as single_card_template:
        single_card_template = single_card_template.read()
    single_card_template = single_card_template.replace('libraryname', library_name)
    single_card_template = single_card_template.replace('path', background_pic_path)

    with open(membership_card_template_path, 'r') as membership_card_template:
        membership_card_template = membership_card_template.read()
    membership_card_template = membership_card_template.replace('libraryname', library_name)

    with open(temp_file_path, 'w+') as temp_file:
        for pk in ids.split(','):
            member = Member.objects.get(pk=pk)
            member_card_template = single_card_template.replace('name', member.user
                                                                .get_full_name())
            if ith_card % 4 == 1 and ith_card != len(ids.split(',')):
                temp_file.write(
                    '\\begin{figure}\n\t\\begin{center}\n' + member_card_template + '\n\n\t\t\\vspace{0.5cm}\n\n')
            elif ith_card % 4 == 0 or ith_card == len(ids.split(',')) - 1:
                temp_file.write(member_card_template + '\n\t\\end{center}\n\\end{figure}\n')
            else:
                temp_file.write(member_card_template + '\n\n\t\t\\vspace{0.5cm}\n\n')
            ith_card += 1

    with open(temp_file_path, 'r') as members_data, open(members_card_path, 'w+') as final:
        final.write(membership_card_template.replace('...', members_data.read()))

    FNULL = open(os.devnull, 'w')
    subprocess.check_call(['xelatex', f'-output-directory={output_dir}', members_card_path])

    # todo find safer way to remove external files:
    # rm -f `ls -I *.pdf`

    return members_card_pdf_path


def generate_single_card(member_id):
    member = Member.objects.get(user_id=member_id)
    templates_path = os.path.join(settings.BASE_DIR, 'reports/templates/reports/latex')

    with open(os.path.join(templates_path, 'single_card.model'), 'r') as single_card, \
            open(os.path.join(templates_path, 'single_card.tex'), 'w') as member_card, \
            open(os.path.join(templates_path, 'card.tex'), 'r') as main_template:
        card_template = single_card.read()
        card_template = card_template.replace('name', member.user.get_full_name())
        card_template = card_template.replace('class', member.user.first_name)
        card_template = card_template.replace('path', os.path.join(templates_path, 'assets/sample_card_template.jpg'))
        member_data = '\\begin{figure}\n\t\\begin{center}\n' + \
                      card_template + \
                      '\n\t\\end{center}\n\\end{figure}\n'
        final_template = main_template.read().replace('...', member_data)
        member_card.write(final_template)

    output_dir = os.path.join(templates_path, 'generated_cards/')
    subprocess.check_call(
        ['xelatex', f'-output-directory={output_dir}', os.path.join(templates_path, 'single_card.tex')])
    return os.path.join(templates_path, 'generated_cards/single_card.pdf')

# todo test
# todo try except
