double coerce(double val, double min, double max);



typedef struct node {
	void *val;
	node *next;
} node;

typedef struct linkedList {
	node *head;
	node *tail;
} linkedList;