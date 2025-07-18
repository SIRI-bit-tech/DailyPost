from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = 'Update the site domain to production domain'

    def handle(self, *args, **options):
        try:
            # Get the default site (ID=1)
            site = Site.objects.get(id=1)
            
            # Update the domain and name
            site.domain = 'www.thedailyrecordpost.com'
            site.name = 'The Daily Record Post'
            site.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully updated site domain to: {site.domain}'
                )
            )
            
        except Site.DoesNotExist:
            # Create the site if it doesn't exist
            site = Site.objects.create(
                id=1,
                domain='www.thedailyrecordpost.com',
                name='The Daily Record Post'
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created site with domain: {site.domain}'
                )
            ) 