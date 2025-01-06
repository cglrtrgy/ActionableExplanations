(define (domain depot)
(:requirements :typing)
(:types place locatable - object
	depot distributor - place
        truck hoist surface - locatable
        pallet crate - surface)

(:predicates (at ?x - locatable ?y - place) 
             (on ?x - crate ?y - surface)
             (in ?x - crate ?y - truck)
             (lifting ?x - hoist ?y - crate)
             (available ?x - hoist)
             (clear ?x - surface))
	

(:action load
:parameters (?x - hoist ?y - crate ?z - truck ?p - place)
:precondition
(and
( at ?z ?p )
( lifting ?x ?y )
( at ?x ?p )

)
:effect
(and
( in ?y ?z )
( available ?x )
(not ( lifting ?x ?y ))
)
)

(:action lift
:parameters (?x - hoist ?y - crate ?z - surface ?p - place)
:precondition
(and
( at ?x ?p )
( clear ?y )
( on ?y ?z )
( at ?y ?p )
( available ?x )

)
:effect
(and
( lifting ?x ?y )
( clear ?z )
(not ( available ?x ))
(not ( on ?y ?z ))
(not ( at ?y ?p ))
(not ( clear ?y ))
)
)

(:action drop
:parameters (?x - hoist ?y - crate ?z - surface ?p - place)
:precondition
(and
( clear ?z )
( lifting ?x ?y )
( at ?z ?p )
( at ?x ?p )

)
:effect
(and
( on ?y ?z )
( clear ?y )
( at ?y ?p )
( available ?x )
(not ( lifting ?x ?y ))
(not ( clear ?z ))
)
)

(:action drive
:parameters (?x - truck ?y - place ?z - place)
:precondition
(and
( at ?x ?y )

)
:effect
(and
( at ?x ?z )
(not ( at ?x ?y ))
)
)

(:action unload
:parameters (?x - hoist ?y - crate ?z - truck ?p - place)
:precondition
(and
( at ?z ?p )
( in ?y ?z )
( at ?x ?p )
( available ?x )

)
:effect
(and
( lifting ?x ?y )
(not ( in ?y ?z ))
(not ( available ?x ))
)
)



)