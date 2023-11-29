# Scores and weights for search function
### Last updated: 2023-11-29

At the re-ranking stage, our search system uses scoring to assign values to each
document based on different parameters. The interplay between clustering and
scoring helps optimize the search process, ensuring that the system considers
both the content and context to deliver more accurate and relevant results for
the user.

This task becomes challenging when dealing with a large number of documents,
creating the need for optimization strategies. A good approach is the
utilization of clustering techniques, which categorize documents based on their
topics, facilitating a more streamlined and efficient search process. We also
use scoring, which involves the assignment of numerical values and weights to
documents based on various parameters, influencing their ranking in the search
results. Here is our different scores, each serving a unique purpose:

1. **Recency**: This score considers the temporal aspect of documents,
   prioritizing recently added or updated content. A document's recency is
   crucial in reflecting the latest information available to users.

1. **Traffic**: The frequency with which users consult a document influences its
   score. Popular or frequently accessed documents are given higher scores,
   indicating their relevance and importance to users. Warning: The home page is
   rated really high since it's where every user land at first.

1. **Current**: This score determines whether a document is currently accessible
   (current=1) or if it has been archived (current=0). It helps users
   distinguish between active and inactive content.

1. **Typicality**: This score evaluates how closely the number of site
   references for a document aligns with the average within a given thematic
   context. Documents with typicality scores reflect a level of correspondence
   with the average number of references, indicating their alignment with the
   common standards within the specified topic. This ensures that the search
   results prioritize documents not only based on their relevance to the user's
   query but also considering how well they conform to the typical reference
   patterns within the targeted theme.

1. **Didactic**: This score evaluates the informational value within content
   chunks that lack a defined structure such as tables. It focuses on the
   quality and depth of information provided without relying on tabular formats
   for organization or presentation. Documents with high didactic scores often
   contain rich textual information, explanations, and details without reliance
   on tabulated data.

1. **Guidance**: This score pertains to content chunks extracted from
   guidance-oriented pages, emphasizing their significance and relevance.
   Guidance pages typically offer comprehensive direction, instruction, or
   expert advice within a specific domain. As these pages tend to provide
   crucial information or instructions sought by users, they are given priority
   to ensure users can readily access the most helpful and directive content.



By incorporating these scoring parameters, we fine-tune the document retrieval
process to align with user needs. It allows us to prioritize documents that are
not only recent, popular, and representative but also closely related to the
user's specific search criteria. This multi-faceted approach enhances the
efficiency and effectiveness of our document retrieval system, ensuring a more
tailored and user-friendly experience.
