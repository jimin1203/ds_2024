#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node {
    int data;
    struct Node* next;
} Node;

typedef struct CircularLinkedList {
    Node* tail;
    int size;
} CircularLinkedList;

Node* createNode(int data) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    if (!newNode) { 
        perror("새 노드에 메모리 할당 실패");
        exit(EXIT_FAILURE);
    }
    newNode->data = data;
    newNode->next = NULL;
    return newNode;
}

void initList(CircularLinkedList* list) {
    list->tail = createNode(-1); 
    list->tail->next = list->tail;
    list->size = 0;
}

void append(CircularLinkedList* list, int data) {
    Node* newNode = createNode(data);
    if (list->size == 0) {
        newNode->next = newNode; 
    } else {
        newNode->next = list->tail->next;
        list->tail->next = newNode;
    }
    list->tail = newNode; 
    list->size++;
}

int removeLRU(CircularLinkedList* list) {
    if (list->size == 0) {
        return -1;
    }
    Node* head = list->tail->next;
    int data = head->data; 
    if (list->size == 1) {
        free(head);
        list->tail = NULL;
    } else {
        list->tail->next = head->next;
        free(head);
    }
    list->size--;
    return data;
}

Node* findNodeAndPrev(CircularLinkedList* list, int data, Node** prevNode) {
    *prevNode = list->tail;
    Node* current = list->tail->next;
    do {
        if (current->data == data) {
            return current;
        }
        *prevNode = current;
        current = current->next;
    } while (current != list->tail->next);
    return NULL; 
}

void simulateLRUCache(char* filename, int cache_size) {
    CircularLinkedList cache;
    initList(&cache);
    int cache_hit = 0;
    int tot_cnt = 0;

    FILE* file = fopen(filename, "r");
    if (!file) {
        perror("파일 열기 실패");
        exit(EXIT_FAILURE);
    }
    
    char line[256];
    while (fgets(line, sizeof(line), file)) {
        int page = atoi(line);
        tot_cnt++;
        Node* prevNode = NULL;
        if (findNodeAndPrev(&cache, page, &prevNode) != NULL) {
            cache_hit++;
            if (cache.size > 1 && prevNode->next != cache.tail) {
                Node* currentPage = prevNode->next;
                prevNode->next = currentPage->next;
                currentPage->next = cache.tail->next;
                cache.tail->next = currentPage;
                cache.tail = currentPage;
            }
        } else {
            if (cache.size >= cache_size) {
                removeLRU(&cache);
            }
            append(&cache, page);
        }
    }
    fclose(file);

    printf("Cache Size: %d ", cache_size);
    printf("Cache Hits: %d ", cache_hit);
    printf("Hit Ratio: %f\n", (double)cache_hit / tot_cnt);
}

int main() {
    char filename[] = "linkbench.trc"; 
    for (int cache_size = 100; cache_size <= 1000; cache_size += 100) {
        CircularLinkedList cache;
        initList(&cache);
        simulateLRUCache(filename, cache_size);
        while (cache.size > 0) {
            removeLRU(&cache);
        }
    }
    return 0;
}

