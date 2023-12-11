# Scores and weights for search function

At the re-ranking stage, our search system uses scoring to assign values to each
document based on different parameters. The interplay between clustering and
scoring helps optimize the search process, ensuring that the system considers
both the content and context to deliver more accurate and relevant results for
the user. 

This task becomes challenging when dealing with a large number of documents,
creating the need for optimization strategies. A good approach is the
utilization of an indexing method called clustering, which categorize documents
based on their topics, facilitating a more streamlined and efficient search
process. We also use scoring, which involves the assignment of numerical values
and weights to documents based on various parameters, influencing their ranking
in the search results. Here is our different scores, each serving a unique
purpose:

1. [**Similarity**](sql/2023-07-19-modify-score_type-add-similarity.sql):
   Represents the primary signal in our scoring mechanism. It denotes the
   measurement of how closely a document aligns with the user's query,
   reflecting the relevance of the document to the search criteria. It is not a
   static precomputed score but a dynamic metric that is computed on the fly
   from the search results. This ensures that the relevance is tied to the
   specific query, going beyond simple keyword matching. Documents with higher
   similarity scores are considered more relevant. By prioritizing similarity as
   the first signal in our scoring process, we aim to deliver search results
   that are more accurate.
      - Scaling: FROM 0.0 = least similar to user query TO 1.0 = most similar to
        user query

1. [**Recency**](sql/schema2.sql.public_new.sql): This score considers the
   temporal aspect of documents, prioritizing recently added or updated content.
   A document's recency is crucial in reflecting the latest information
   available to users. 
      - Scaling: FROM 0.0 = oldest document TO 1.0 = most recent document

1. [**Traffic**](sql/compute-traffic-score.sql): The frequency with which users
   consult a document influences its score. Popular or frequently accessed
   documents are given higher scores with the help of web traffic logs,
   indicating their relevance and importance to users. Warning: The home page is
   rated really high since it's where every user land at first.
      - Scaling: FROM 0.0 = least consulted document TO 1.0 = most consulted
        document

1. [**Current**](sql/2023-07-12-score-current.sql): This score determines
   whether a document is currently accessible or if it has been archived. It
   helps users distinguish between active and inactive content.
      - Scaling: 0.0 = currently accessible document **OR** 1.0 = archived
        document

1. [**Typicality**](sql/2023-07-12-calculate-incoming-outgoing-counts.sql): This
   score evaluates how closely the number of site references for a document
   aligns with the average. Documents with typicality scores reflect a level of
   correspondence with the average number of references. This ensures that the
   search results prioritize documents considering how well they conform to the
   typical reference patterns within the targeted theme.
      - Scaling: FROM 0.0 = least referenced document TO 1.0 = most referenced
        document

1. **Didactic**: This score evaluates the informational value within content
   chunk. It scores higher based the quality and readability of information
   provided. Documents with high didactic scores often contain rich textual
   information, explanations, and details. Implementation of the score looks for
   signs of the opposite to compute its score - for example, the presence of a
   large proportion of tabular data which indicate data dumps from spreadsheets
   or databases.
      - Scaling: FROM 0.0 = mostly tabular data or information that is not
        expected to be read sequentially by a user TO 1.0 = contains rich
        textual information, explanations, and details

1. **Guidance**: This score pertains to content chunks extracted from
   guidance-oriented pages, emphasizing their significance and relevance.
   Guidance pages typically offer comprehensive direction, instruction, or
   expert advice within a specific domain. As these pages tend to provide
   crucial information or instructions sought by users, they are given priority
   to ensure users can readily access the most helpful and directive content.
      - FROM Scaling: 0.0 = doesn't include crucial information or instructions
        TO 1.0 = includes crucial information or instructions

By incorporating these scoring parameters, we fine-tune the document retrieval
process to align with user needs. It allows us to prioritize documents that are
not only recent, popular, and representative but also closely related to the
user's specific search criteria. This multi-faceted approach enhances the
efficiency and effectiveness of our document retrieval system, ensuring a more
tailored and user-friendly experience.

## Future

In addition to our current considerations, we can explore the integration of
thematic context into our scoring system. Thematic context involves a specific
focus on the subject or theme related to the user's query, ensuring that the
context is taken into account during the initial score calculation. To implement
this, we would need to incorporate topic labels for documents, a feature not yet
incorporated in our system. Planning for such additional scores allows us to
enhance the depth and relevance of our responses by considering the specific
themes associated with user queries.
