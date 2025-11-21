import ailab.db as db

from ailab.db.finesse.test_queries import get_random_document_score


class NoChunkFoundError(Exception):
    pass


## This is a comment.
def evaluate_random_document(project_db):  
  
    if project_db is None:  
        print("Database connection failed.")  
        return None  
  
    with project_db.cursor() as cursor:  
  
        random_chunk = get_random_document_score(cursor, "louis_v005")  
  
        if not random_chunk:  
            raise NoChunkFoundError("No chunk found in the database.")  
  
        print("\n-------------")
        print("crawl_id:", random_chunk[0]["crawl_id"])  
        print("crawl_url:", random_chunk[0]["crawl_url"])
        print("\n") 
        
        print("-------------")
        for chunk in random_chunk:  
            print("score_type:", chunk["score_type"])  
            print("score:", chunk["score"])  
            print("\n")  
        
    return  



def main():
    project_db = db.connect_db()
    evaluate_random_document(project_db)


if __name__ == "__main__":
    main()
