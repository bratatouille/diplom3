from django.db import models

# Create your models here.

class HeroSlide(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    subtitle = models.CharField('Подзаголовок', max_length=300, blank=True)
    image = models.ImageField('Картинка', upload_to='hero_slides/', blank=True, null=True)
    button1_text = models.CharField('Текст кнопки 1', max_length=50, blank=True)
    button1_url = models.URLField('Ссылка кнопки 1', blank=True)
    button2_text = models.CharField('Текст кнопки 2', max_length=50, blank=True)
    button2_url = models.URLField('Ссылка кнопки 2', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    active = models.BooleanField('Активен', default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Слайд карусели'
        verbose_name_plural = 'Слайды карусели'

    def __str__(self):
        return self.title

class Advantage(models.Model):
    ICON_CHOICES = [
        ('star', 'Звезда'),
        ('shield', 'Щит'),
        ('support', 'Поддержка'),
        ('rocket', 'Ракета'),
        ('gift', 'Подарок'),
        ('heart', 'Сердце'),
    ]
    icon = models.CharField('Иконка', max_length=20, choices=ICON_CHOICES, default='star')
    color = models.CharField('Цвет иконки (hex)', max_length=20, default='#7a85ff')
    title = models.CharField('Заголовок', max_length=100)
    description = models.CharField('Описание', max_length=300)
    order = models.PositiveIntegerField('Порядок', default=0)
    active = models.BooleanField('Активен', default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Преимущество'
        verbose_name_plural = 'Преимущества'

    def __str__(self):
        return self.title

class SupportTicket(models.Model):
    TOPIC_CHOICES = [
        ('general', 'Общий вопрос'),
        ('order', 'Вопрос по заказу'),
        ('delivery', 'Вопрос по доставке'),
        ('return', 'Вопрос по возврату'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('in_progress', 'В обработке'),
        ('resolved', 'Решен'),
        ('closed', 'Закрыт'),
    ]
    
    name = models.CharField('Имя', max_length=100)
    email = models.EmailField('Email')
    topic = models.CharField('Тема', max_length=20, choices=TOPIC_CHOICES, default='general')
    message = models.TextField('Сообщение')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлен', auto_now=True)
    response = models.TextField('Ответ', blank=True)
    
    class Meta:
        verbose_name = 'Тикет поддержки'
        verbose_name_plural = 'Тикеты поддержки'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Тикет #{self.id} - {self.name} ({self.get_topic_display()})'
