# UN!TE Framework for Creating Cyber Defense Collaboration Playbooks
_This is a draft/experimental framework under development. Not intended for operational use, yet. Please stay tuned for a usable version. Feedback is welcome!_
### Overview
Detecting and mitigating cyber threat campaigns often requires collaboration across industry, government, and private threat researchers.  To help scale these defensive operations globally, the UN!TE framework is a standardized set of collaboration actions that allows for easy creation of team playbooks.  
### Who Can Use UN!TE?
National CERTs, threat research teams, and others can use these playbooks to organize defensive campaigns with specific roles for organization types like potential target companies, cybersecurity service providers, internet ecosystem providers, and government agencies.  Each of these organization types have different capabilities and data set that can be brought to the table for responding to a major cybersecurity event, such as a nation-state threat campaign or national response to a major new vulnerability. 
### Integration with sharing platforms
A current focus of the project is to integrate into infromation sharing platforms to enable easy creation and execution of playbooks by threat researchers. 
### Core Framework
The core framework is a JSON file that includes two sets of data: defensive partners and collaborative actions.
```
Header
Defensive Partners - List and details of partner types for playbook actions
Collaborative Actions – List and details of actions to be included in playbooks
```
**Defensive Partners** are the various partner types that participate in collaborative cyber defense operations. Often these organization types have different capabilities and data holdings that can be brought to bear during collaborative efforts.  
**Collaboration Actions** are the specific activities that partners do to collaboratively detect and mitigate threat campaigns.  
### Playbook Format
When sharing indicators or coordinating collaborative defensive campaigns, National CERTs, threat research teams, and others can use the framework to create playbooks of recommended actions. 
```
Header
Defensive Partners
Actions
```
### Playbook Examples
- **[Log4j Critical Vulnerability Response (CVE-2021-44228)](playbooks/log4j-critical-vulnerability-response.md)** - A real-world annotated playbook showing how UN!TE's defensive partners and collaborative actions worked together during the Log4j/Log4Shell incident. This playbook demonstrates the framework mapping to an actual multi-partner cyber defense collaboration.
### How is UN!TE Different than Other Frameworks?
UN!TE focuses on actions that can be taken as a defensive team across multiple organizations.  It seeks to *leverage and be paired with* other existing frameworks like MITRE ATT&CK, STIX/TAXII, the Incident Command Structure, CSIRT Services Framework, and CACAO.
### Authors & Contributors
[@peterxsu](https://github.com/peterxsu)

[@grotemr](https://github.com/grotemr) 
