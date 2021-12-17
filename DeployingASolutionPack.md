# Deploying a Solution Pack

1. Login to the GIT repo [https://github.com/fortinet-fortisoar/](https://github.com/fortinet-fortisoar/), which contains the solution packs, using your credentials.
2. In the **Find a repository** field, type the name of solution pack repository, or navigate to the solution pack repository that you want to deploy and click on the same.    
   As an example, we are going to deploy the Mitre Attack Solution pack (solution-pack-mitre-attack)  
   ![Finding a Solution Pack Repository](media/findingarepo.png)
3. On the solution pack's page, click **Releases**, which displays the list of releases for that solution pack:  
   ![Solution Pack Page - Releases](media/spPageReleases.png)
4. On the solution pack's Releases page, choose the solution pack release you want to deploy and download the respective zip files.     
   ![Choosing the release of the solution pack you want to deploy](media/spReleasesChooseRelease.png)
5. Log on to your FortiSOAR instance, and perform the following steps to import the solution pack:
    1. Click **System Settings** and then from the left-navigation, click **Import Wizard**  
       ![Import Wizard option in left navigation](media/importWiz.png) 
    2. On the `Import Wizard` page, click **Import From File** and selected the solution pack zip that you have downloaded, and navigate through the Import Wizard.   
       ![Importing a Solution Pack zip file](media/importIRCP.png)  
       **Note**: It is recommended not the change any configurations or options of the imported solution pack zip file.  

    Once the import is successfully completed, you can use the solution pack.

