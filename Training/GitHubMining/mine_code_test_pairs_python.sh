# Установка переменной in_file в значение 'python-top-repos.txt'
in_file=${1:-"python-top-repos.txt"}

# Установка переменной language в значение 'python'
language=python


# Извлечение первых 148000 строк из файла python-top-repos.txt
head -1000 $in_file |

# Использование xargs для выполнения команды для каждой строки из предыдущего вывода
# xargs -P32 -n1 -I% bash -c '
xargs -P32 -n1 -I% bash -c '
    # Вывод текущей строки
    echo %;

    # Разбиение строки на компоненты
    line=%;
    line_array=($line);
    github_link=${line_array[0]};

    # Запуск скрипта cloner_current_state.sh для клонирования репозитория из GitHub
    ./cloner_current_state.sh $github_link '$language';

    # Запуск скрипта extract_pairs.sh для извлечения пар тестовых исходных файлов
    ./extract_pairs.sh $github_link '$language';
' 

# Комментарий: Запуск скрипта mine_code_test_pairs_python.sh, вывод результата в output_mine_python.txt
# unbuffer ./mine_code_test_pairs_python.sh 2>&1 | tee output_mine_python.txt


# --- Old code ---
# language=python
# in_file=python-top-repos.txt
# head -148000 $in_file | xargs -P32 -n1 -I% bash -c 'echo %; \
# line=$"%";\
# line_array=($line);\
# github_link=${line_array[0]};\
# ./cloner_current_state.sh $github_link '$language'; \
# ./extract_pairs.sh $github_link '$language

# # unbuffer ./mine_code_test_pairs_python.sh 2>&1 | tee output_mine_python.txt