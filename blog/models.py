from django.db import models
from django.utils import timezone


class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name='аголовок')
    content = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blog/previews/', verbose_name='ревью', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name='ата создания')
    is_published = models.BooleanField(default=True, verbose_name='ризнак публикации')
    views_count = models.PositiveIntegerField(default=0, verbose_name='оличество просмотров')
    
    class Meta:
        verbose_name = 'логовая запись'
        verbose_name_plural = 'логовые записи'
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
