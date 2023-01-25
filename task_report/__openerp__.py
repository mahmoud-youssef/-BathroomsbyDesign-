{
    'name' : 'IM Bus',
    'version': '1.0',
    'author': 'OpenERP SA',
    'category': 'Hidden',
    'complexity': 'easy',
    'description': "Instant Messaging Bus allow you to send messages to users, in live.",
    'depends': ['base', 'web','project'],
    'data': [
        'views/task_report.xml',
        # 'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': True,
}
