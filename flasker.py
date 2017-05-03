from flask import Flask, render_template, request, redirect, url_for
import csv
import os.path
app = Flask(__name__, static_url_path='/static')


def delete_data(s_id):
    datas = load_datas('datas.csv')
    for data in datas:
        if data[0] == str(s_id):
            datas.remove(data)
    write_list_to_csv(datas)


def load_datas(filename):
    datas_for_id = []
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                datas_for_id.append(row)
    return datas_for_id


def write_csv(datas):
    filename = 'datas.csv'
    datas_for_id = []
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                datas_for_id.append(row)
        s_id = int(datas_for_id[len(datas_for_id) - 1][0]) + 1
        datas[0] = str(s_id)
        with open(filename, 'a') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(datas)
    else:
        datas[0] = 1
        write_list_to_csv(datas)


def write_list_to_csv(datas):
    filename = 'datas.csv'
    with open(filename, 'w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerows(datas)


def d_update(datas):
    s_id = datas[0]
    file_datas = load_datas('datas.csv')
    for i in range(len(file_datas)):
        if s_id == file_datas[i][0]:
            for j in range(1, 7):
                file_datas[i][j] = datas[j]
    write_list_to_csv(file_datas)


@app.route('/story', methods=['POST', 'GET'])
def story_add_page():
    if request.method == 'POST':
        datas = []
        datas.append('0')
        datas.append(request.form['s_title'])
        datas.append(request.form['s_text'])
        datas.append(request.form['criteria'])
        datas.append(request.form['bval'])
        datas.append(request.form['est'])
        datas.append(request.form['status'])
        write_csv(datas)
        return redirect(url_for('list_page'))
    data_tmp = []
    return render_template('form.html', story=data_tmp, typ='A')


@app.route('/story/<story_id>', methods=['POST', 'GET'])
def stroy_view_page(story_id=None):
    if request.method == 'POST':
        getted_datas = []
        getted_datas.append(story_id)
        getted_datas.append(request.form['s_title'])
        getted_datas.append(request.form['s_text'])
        getted_datas.append(request.form['criteria'])
        getted_datas.append(request.form['bval'])
        getted_datas.append(request.form['est'])
        getted_datas.append(request.form['status'])
        d_update(getted_datas)
        return redirect(url_for('list_page'))
    datas = load_datas('datas.csv')
    data_tmp = []
    for i in range(len(datas)):
        if datas[i][0] == story_id:
            for j in range(len(datas[i])):
                data_tmp.append(datas[i][j])
    return render_template('form.html', story=data_tmp, typ='V', s_id=story_id)


@app.route('/del/<story_id>')
def del_story(story_id=None):
    delete_data(story_id)
    return redirect(url_for('list_page'))


@app.route('/list')
def list_page():
    datas = load_datas('datas.csv')
    return render_template('list.html', datas=datas)


def main():
    pass


if __name__ == '__main__':
    main()
