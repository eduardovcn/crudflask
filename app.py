from flask import Flask, request, jsonify
from models.task import Task


#__name__ = __main__
app = Flask(__name__)

#CRUD
#CREATE, READ, UPDATE, DELETE
#Tabela: Tarefa

tasks = []
task_id_control = 1

@app.route("/tasks", methods=["POST"]) #Criar uma nova tarefa
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control ,title=data["title"], description=data.get("description", "")) #get() para pegar o valor de uma chave que pode não existir
    tasks.append(new_task)
    task_id_control += 1
    print(tasks)
    print(data)
    return jsonify({"message": "Nova tarefa criada com sucesso"})

@app.route("/tasks", methods=["GET"]) #Listar todas as tarefas
def get_tasks():
    task_list = [task.to_dict() for task in tasks]
   
    output = {
        "tasks": task_list,
        "total_tasks": len(task_list)
         }
    return jsonify(output)

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = None #não foi necessário neste caso. Mas é uma boa prática
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())
    return jsonify({"message": "Tarefa não encontrada"}), 404

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
    print(task)

    if task == None:
        return jsonify({"message": "Tarefa não encontrada"}), 404
    
    data = request.get_json()
    task.title = data['title']
    task.description = data['description']
    task.completed = data['completed']
    print(task)
    #identificador não se atualiza para nao perder o rastreio

    return jsonify({"message": "Tarefa atualizada com sucesso"})

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break
    
    if not task:
        return jsonify({"message": "Tarefa não encontrada"}), 404
    
    tasks.remove(task)
    return jsonify({"message": "Tarefa deletada com sucesso"})

  

if __name__ == "__main__":
    app.run(debug=True)
