from invoke import task
import shutil


@task
def dist(context):
    shutil.rmtree("./dist", ignore_errors=True)
    context.run("python setup.py sdist")
    context.run("python setup.py bdist_wheel")


@task
def test(context):
    with context.cd("tests"):
        context.run("pytest .")
