from flask import Blueprint, request, jsonify, send_file
from App.models import obter_tarefas, criar_tarefa, atualizar_tarefa, deletar_tarefa
from App.sqs import enviar_mensagem_sqs
from App.s3 import fazer_upload_s3, baixar_arquivo_s3
import uuid
from flasgger import swag_from

main = Blueprint('main', __name__)

@main.route('/tarefas', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'Lista de tarefas',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'string'},
                        'task': {'type': 'string'},
                        'completed': {'type': 'boolean'}
                    }
                }
            }
        }
    }
})
def obter_todas_tarefas():
    tarefas = obter_tarefas()
    return jsonify(tarefas)

@main.route('/tarefas', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'task': {'type': 'string'},
                    'completed': {'type': 'boolean'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Tarefa criada'
        }
    }
})
def criar_nova_tarefa():
    tarefa = request.json
    tarefa_id = str(uuid.uuid4())
    tarefa['id'] = tarefa_id
    criar_tarefa(tarefa)
    enviar_mensagem_sqs('TarefaCriada', tarefa)
    return '', 201

@main.route('/tarefas/<tarefa_id>', methods=['PUT'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'task': {'type': 'string'},
                    'completed': {'type': 'boolean'}
                }
            }
        }
    ],
    'responses': {
        204: {
            'description': 'Tarefa atualizada'
        }
    }
})
def atualizar_tarefa_existente(tarefa_id):
    tarefa_atualizada = request.json
    atualizar_tarefa(tarefa_id, tarefa_atualizada)
    enviar_mensagem_sqs('TarefaAtualizada', tarefa_atualizada)
    return '', 204

@main.route('/tarefas/<tarefa_id>', methods=['DELETE'])
@swag_from({
    'responses': {
        204: {
            'description': 'Tarefa deletada'
        }
    }
})
def deletar_tarefa_existente(tarefa_id):
    deletar_tarefa(tarefa_id)
    enviar_mensagem_sqs('TarefaDeletada', {'id': tarefa_id})
    return '', 204

@main.route('/tarefas/<tarefa_id>/upload', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'Arquivo para upload'
        }
    ],
    'responses': {
        201: {
            'description': 'Arquivo enviado',
            'schema': {
                'type': 'object',
                'properties': {
                    'url': {'type': 'string'}
                }
            }
        }
    }
})
def fazer_upload_arquivo(tarefa_id):
    if 'file' not in request.files:
        return 'Nenhum arquivo selecionado', 400
    file = request.files['file']
    if file.filename == '':
        return 'Nenhum arquivo selecionado', 400
    file_url = fazer_upload_s3(file)
    return jsonify({'url': file_url}), 201

@main.route('/tarefas/<tarefa_id>/download/<filename>', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'Arquivo baixado'
        }
    }
})
def baixar_arquivo(tarefa_id, filename):
    file_path = baixar_arquivo_s3(filename)
    return send_file(file_path)
