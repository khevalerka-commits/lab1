% ============================================================
% Лабораторная работа 10. Логическое программирование в SWI-Prolog
% Дисциплина: Парадигмы программирования
% Вариант 3: Учебный план, основной предикат next_course/2
% Запуск:  swipl lab10.pl      затем  ?- demo.
% ============================================================

% ------------------------------------------------------------
% Исходная база знаний
% ------------------------------------------------------------

% student(Name)
student(aida).
student(miras).
student(dana).
student(timur).
student(aliya).          % Задание 1: новый студент

% course(Name)
course(programming_1).
course(programming_2).
course(data_structures).
course(databases).
course(artificial_intelligence).
course(machine_learning).

% completed(Student, Course)
completed(aida, programming_1).
completed(aida, programming_2).
completed(aida, data_structures).
completed(aida, databases).
completed(miras, programming_1).
completed(miras, databases).
completed(dana, programming_1).
completed(dana, programming_2).
completed(dana, data_structures).
completed(timur, programming_1).
completed(aliya, programming_1).   % Задание 1
completed(aliya, programming_2).   % Задание 1

% requires(Course, Prerequisite)
requires(programming_2, programming_1).
requires(data_structures, programming_2).
requires(artificial_intelligence, data_structures).
requires(artificial_intelligence, databases).
requires(machine_learning, artificial_intelligence).

% Эксперимент задания 7 (временно раскомментировать, затем вернуть):
% requires(programming_1, machine_learning).

% ------------------------------------------------------------
% Задание 2. Правила и составные цели
% ------------------------------------------------------------

ai_candidate(Student) :-
    completed(Student, data_structures),
    completed(Student, databases).

strong_student(Student) :-
    completed(Student, programming_2),
    completed(Student, data_structures).

% ------------------------------------------------------------
% Задание 4. Непосредственный допуск
% ------------------------------------------------------------

missing_direct(Student, Course, Prerequisite) :-
    student(Student),
    requires(Course, Prerequisite),
    \+ completed(Student, Prerequisite).

immediate_eligible(Student, Course) :-
    student(Student),
    course(Course),
    \+ missing_direct(Student, Course, _).

% ------------------------------------------------------------
% Задание 5. Транзитивные пререквизиты
% (сначала базовый случай, затем рекурсивный)
% ------------------------------------------------------------

prerequisite(Course, Prerequisite) :-
    requires(Course, Prerequisite).
prerequisite(Course, Prerequisite) :-
    requires(Course, Intermediate),
    prerequisite(Intermediate, Prerequisite).

% ------------------------------------------------------------
% Задание 6. Полный допуск и список недостающих курсов
% Student и Course должны быть заданы к моменту вызова.
% Результат setof сначала сохраняется в Found и только после
% отсечения унифицируется с Missing. В исходной версии из
% методички Missing передавался прямо в setof, из-за чего
% вызов missing_all(miras, artificial_intelligence, []) падал
% во второй клаузе и ошибочно возвращал true.
% ------------------------------------------------------------

missing_all(Student, Course, Missing) :-
    setof(P,
          ( prerequisite(Course, P),
            \+ completed(Student, P) ),
          Found),
    !,
    Missing = Found.
missing_all(_, _, []).

eligible(Student, Course) :-
    student(Student),
    course(Course),
    missing_all(Student, Course, []).

% ------------------------------------------------------------
% Задание 7. Безопасный обход с контролем посещённых курсов
% ------------------------------------------------------------

safe_prerequisite(Course, Prerequisite) :-
    safe_prerequisite(Course, Prerequisite, [Course]).

safe_prerequisite(Course, Prerequisite, _) :-
    requires(Course, Prerequisite).
safe_prerequisite(Course, Prerequisite, Visited) :-
    requires(Course, Next),
    \+ memberchk(Next, Visited),
    safe_prerequisite(Next, Prerequisite, [Next|Visited]).

% ------------------------------------------------------------
% Задание 8. Интегрированный отчёт
% student/1 и course/1 привязывают переменные до вызова
% missing_all/3, поэтому предикат работает и для запросов
% вида recommendation(Student, Course, Status, Missing).
% ------------------------------------------------------------

recommendation(Student, Course, eligible, []) :-
    student(Student),
    course(Course),
    eligible(Student, Course).
recommendation(Student, Course, missing, Missing) :-
    student(Student),
    course(Course),
    missing_all(Student, Course, Missing),
    Missing \= [].

% ------------------------------------------------------------
% Индивидуальный вариант 3: учебный план
% next_course(Student, Course): курс ещё не освоен студентом
% и все его прямые и косвенные пререквизиты освоены.
% ------------------------------------------------------------

not_completed(Student, Course) :-
    student(Student),
    course(Course),
    \+ completed(Student, Course).

next_course(Student, Course) :-
    not_completed(Student, Course),
    eligible(Student, Course).

next_courses(Student, Courses) :-
    student(Student),
    findall(C, next_course(Student, C), Courses).

blocked_course(Student, Course, Missing) :-
    not_completed(Student, Course),
    missing_all(Student, Course, Missing),
    Missing \= [].

finished_program(Student) :-
    student(Student),
    \+ not_completed(Student, _).

% ------------------------------------------------------------
% Демонстрация: ?- demo.
% Для каждой цели печатаются все решения (аналог нажатия «;»).
% ------------------------------------------------------------

demo :-
    forall(demo_goal(G), show(G)).

show(G) :-
    format("?- "),
    portray_clause(G),
    findall(G, call(G), Solutions),
    (   Solutions == []
    ->  writeln('   false.')
    ;   forall(member(S, Solutions),
               ( format("   "), portray_clause(S) ))
    ),
    nl.

% Задание 1
demo_goal(completed(aida, databases)).
demo_goal(completed(_, programming_1)).
demo_goal(completed(aliya, programming_2)).
demo_goal(completed(aliya, databases)).
% Задание 2
demo_goal(ai_candidate(_)).
demo_goal(strong_student(_)).
% Задание 3
demo_goal(record(_, _) = record(aida, databases)).
demo_goal(pair(_X, _X) = pair(aida, miras)).
demo_goal([_|_] = [programming_1, databases, ai]).
% Задание 4
demo_goal(missing_direct(miras, artificial_intelligence, _)).
demo_goal(immediate_eligible(aida, artificial_intelligence)).
demo_goal(immediate_eligible(miras, artificial_intelligence)).
demo_goal(immediate_eligible(dana, artificial_intelligence)).
% Задание 5
demo_goal(prerequisite(machine_learning, _)).
demo_goal(prerequisite(artificial_intelligence, programming_1)).
demo_goal(prerequisite(artificial_intelligence, _)).
% Задание 6
demo_goal(missing_all(miras, artificial_intelligence, _)).
demo_goal(eligible(aida, artificial_intelligence)).
demo_goal(eligible(miras, artificial_intelligence)).
% Задание 7
demo_goal(safe_prerequisite(machine_learning, _)).
% Задание 8
demo_goal(recommendation(_, artificial_intelligence, _, _)).
demo_goal(recommendation(_, machine_learning, _, _)).
% Вариант 3
demo_goal(next_course(aida, _)).
demo_goal(next_course(timur, _)).
demo_goal(next_courses(miras, _)).
demo_goal(next_courses(aliya, _)).
demo_goal(blocked_course(miras, _, _)).
demo_goal(next_course(_, databases)).
demo_goal(next_course(aida, machine_learning)).
demo_goal(next_course(aida, databases)).
demo_goal(finished_program(aida)).
