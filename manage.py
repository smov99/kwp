a
    E[`�  �                   @   s.   d Z ddlZddlZdd� Zedkr*e�  dS )z7Django's command-line utility for administrative tasks.�    Nc               
   C   s\   t j�dd� zddlm}  W n. tyL } ztd�|�W Y d}~n
d}~0 0 | tj� dS )zRun administrative tasks.�DJANGO_SETTINGS_MODULEzconfig.settingsr   )�execute_from_command_linez�Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?N)�os�environ�
setdefault�django.core.managementr   �ImportError�sys�argv)r   �exc� r   �4F:/workspace/django/kiwapower_web_proposal\manage.py�main   s    ��r   �__main__)�__doc__r   r	   r   �__name__r   r   r   r   �<module>   s
   