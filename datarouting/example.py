import sys
from route import Router

router = Router([
        {
            'name': 'udpate_svn_and_import'
            },
        {
            'name': 'move_new_data'
            },
        
        {
            'name': 'make_reduced_data'
            },
        
        {
            'name': 'pack_txt'
            },
        {
            'name': 'sa_sweeps_tables'
            },
        {
            'name': 'sa_time_tables_cpu',
            'spin_flip_rate': 6.5e9
            },
        {
            'name': 'dwave_anneal_time_table'
            },
        {
            'name': 'scaling_ctq'
            },
        {
            'name': 'scaling_dtq'
            },
        {
            'name': 'scaling_dwave'
            },

        {
            'name': 'make_backup_to_archive'
            },

        {
            'name': 'make_backup_to_server'
            },

])


