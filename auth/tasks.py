from invoke.tasks import task

@task
def new_migration(ctx, name: str):
    ctx.run(f'docker-compose run auth_service alembic revision --autogenerate -m {name}')

@task
def apply_migration(ctx):
    ctx.run('docker-compose run auth_service alembic upgrade head')
    
@task
def build(ctx):
    ctx.run('docker-compose build')

@task
def up(ctx):
    ctx.run('docker-compose up')

@task
def down(ctx):
    ctx.run('docker-compose down')

@task
def test(ctx):
    ctx.run('docker-compose run auth_service pytest')
