from flask import render_template, request, redirect, url_for, flash
from app import app, mysql

@app.route('/')
def index():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nome, descricao FROM item")
        items = cur.fetchall()
        
        # Verifica se há resultados e formata corretamente
        if items:
            items_list = []
            for item in items:
                # Acessa os valores pelo nome da coluna (devido ao DictCursor)
                items_list.append({
                    'id': item['id'],
                    'nome': item['nome'],
                    'descricao': item.get('descricao', '')
                })
            return render_template("index.html", items=items_list)
        else:
            return render_template("index.html", items=[])
            
    except Exception as e:
        app.logger.error(f"Erro na rota index: {str(e)}")
        return render_template("index.html", items=[])
        
    finally:
        if 'cur' in locals():
            cur.close()


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        cur = None
        try:
            nome = request.form.get('nome', '').strip()
            descricao = request.form.get('descricao', '').strip()
            
            if not nome:
                flash("O nome é obrigatório", "warning")
                return render_template('create.html')
            
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO item (nome, descricao) VALUES (%s, %s)",
                (nome, descricao)
            )
            mysql.connection.commit()
            
            flash("Item criado com sucesso!", "success")
            return redirect(url_for('index'))
            
        except Exception as e:
            mysql.connection.rollback()
            app.logger.error(f"Erro ao criar item: {str(e)}")
            flash("Erro interno ao criar item", "danger")
            return render_template('create.html')
            
        finally:
            if cur:
                cur.close()
    
    return render_template('create.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    cur = None
    try:
        cur = mysql.connection.cursor()
        
        if request.method == 'POST':
            nome = request.form.get('nome', '').strip()
            descricao = request.form.get('descricao', '').strip()
            
            if not nome:
                flash("O nome é obrigatório", "warning")
                return redirect(url_for('update', id=id))
            
            # Debug: Mostrar valores recebidos
            app.logger.info(f"Atualizando item {id} com nome: {nome}, descrição: {descricao}")
            
            cur.execute(
                "UPDATE item SET nome = %s, descricao = %s WHERE id = %s",
                (nome, descricao, id)
            )
            mysql.connection.commit()
            
            flash("Item atualizado com sucesso!", "success")
            return redirect(url_for('index'))
        
        # GET Request - Busca o item para edição
        cur.execute("SELECT id, nome, descricao FROM item WHERE id = %s", (id,))
        item = cur.fetchone()
        
        if not item:
            flash("Item não encontrado", "danger")
            return redirect(url_for('index'))
            
        # Debug: Mostrar item encontrado
        app.logger.info(f"Item encontrado para edição: {item}")
        
        return render_template('update.html', item={
            'id': item['id'],
            'nome': item['nome'],
            'descricao': item.get('descricao', '')
        })
        
    except Exception as e:
        mysql.connection.rollback()
        app.logger.error(f"Erro ao atualizar item {id}: {str(e)}", exc_info=True)
        flash(f"Erro ao atualizar item: {str(e)}", "danger")
        return redirect(url_for('index'))
        
    finally:
        if cur:
            cur.close()

@app.route('/delete/<int:id>')
def delete(id):
    cur = None
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM item WHERE id = %s", (id,))
        if not cur.fetchone():
            flash("Item não encontrado", "warning")
            return redirect(url_for('index'))
            
        cur.execute("DELETE FROM item WHERE id = %s", (id,))
        mysql.connection.commit()
        flash("Item excluído com sucesso!", "success")
        
    except Exception as e:
        mysql.connection.rollback()
        app.logger.error(f"Erro ao excluir item {id}: {str(e)}")
        flash("Erro interno ao excluir item", "danger")
        
    finally:
        if cur:
            cur.close()
    
    return redirect(url_for('index'))

@app.route('/health')
def health_check():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        return "OK", 200
    except Exception as e:
        return str(e), 500
    finally:
        cur.close()