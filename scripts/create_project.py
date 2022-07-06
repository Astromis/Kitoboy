"""
File contains scripts for create projects
throw api and change their status
to start use   python3 create_project.py -m dev   (pr prod)
 """
import sys
import argparse
from random import randint

sys.path.append('/var/www/labeling_service/backend')
from utils.api_client import ApiClient

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', help='dev or prod')
    args = parser.parse_args()

    host = 'http://0.0.0.0:8000' if args.mode == 'dev' else 'http://89.22.186.2:7380'

    params = [{'title': f'title {i}', 'description': f'description {i}',
               'type_name': 'audio_transcription', 'amount': 1,
               'dataset_id': 3,
               'priority_id': 1, 'guideline_id': 1, 'product_id': randint(1, 3)}
              for i in range(1)]

    # Главный проект
    main_params = {

        'title': 'main test', 'description': 'main test Description',
        'priority_id': 1, 'product_id': 1,

    }
    # Зависимости главного проекта
    rel_params = {'main_project_id': '',
                  'projects': {
                      1: [],
                      2: [],
                  }}
    api_cl = ApiClient('admin')
    api_cl.host = host

    for idx, param in enumerate(params):
        res = api_cl.manage_project(param, proj_type='audio/transcription')
        rel_params['projects'][1].append(
            {'id': res['project_id'], 'type': param['type_name'],
             'related': None})

    # верификация для первой задачи audio_transcription
    verify = {'verifier_id': 4, 'action': 1,
              'project_id': res['project_id'], 'total_percent': 30}
    verify_id = api_cl.manage_verify_task(params=verify,
                                          v_type='audio_transcription')[
        'verify_id']

    text_params = [
        {'title': f'ner title {i}', 'description': f'ner description {i}',
         'type_name': 'text_labeling', 'amount': 1,
         'product_id': randint(1, 3), 'dataset_id': 1,
         'priority_id': 1, 'guideline_id': 1, 'due_date': '2020-04-20',
         'label_color_ids': [lbl for lbl in range(1, 7)]} for i in
        range(1, 2)]

    for idx, param in enumerate(text_params):
        # usr = users[idx % 2]
        # Корневая задача text_labeling
        res = api_cl.manage_project(param, proj_type='text/ner')
        rel_params['projects'][1].append(
            {'id': res['project_id'], 'type': param['type_name'],
             'related': None})
        # Зависимая задача text_labeling от audio_transcription
        res_2 = api_cl.manage_project(param, proj_type='text/ner')
        rel_params['projects'][2].append(
            {'id': res_2['project_id'], 'type': param['type_name'],
             'related': 1})

    # верификация для 2ой задачи text_labeling
    verify_ner = {'verifier_id': 4, 'action': 1, 'total_percent': 30,
                  'project_id': res_2['project_id']}
    verify_id_ner = api_cl.manage_verify_task(params=verify_ner,
                                              v_type='text_labeling')[
        'verify_id']
    # Создание главного проекта, 1 text_labeling создадутся после разметки
    # 1ого audio_transcription
    main_project_id = api_cl.create_main_project(main_params)['main_project_id']

    rel_params['main_project_id'] = main_project_id
    # Создание связей между подпроектами
    api_cl.create_relations_project(rel_params)
    # Создание задач для корневых подпроектов
    api_cl.start_projects({'projects': rel_params['projects'][1]})
