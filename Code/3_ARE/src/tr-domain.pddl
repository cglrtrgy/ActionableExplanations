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
	

(:action unload
:parameters (?x - hoist ?y - crate ?z - truck ?p - place)
:precondition
(and
( at ?z ?p )
( in ?y ?z )
( available ?x )

)
:effect
(and
( lifting ?x ?y )
(not ( available ?x ))
(not ( in ?y ?z ))
)
)

(:action lift
:parameters (?x - hoist ?y - crate ?z - surface ?p - place)
:precondition
(and
( at ?x ?p )
( on ?y ?z )
( available ?x )
( at ?y ?p )
( clear ?y )

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

(:action drop
:parameters (?x - hoist ?y - crate ?z - surface ?p - place)
:precondition
(and
( clear ?z )
( at ?x ?p )
( at ?z ?p )
( lifting ?x ?y )

)
:effect
(and
( clear ?y )
( available ?x )
( on ?y ?z )
( at ?y ?p )
(not ( clear ?z ))
(not ( lifting ?x ?y ))
)
)

(:action load
:parameters (?x - hoist ?y - crate ?z - truck ?p - place)
:precondition
(and
( lifting ?x ?y )
( at ?x ?p )
( at ?z ?p )

)
:effect
(and
( in ?y ?z )
( available ?x )
(not ( lifting ?x ?y ))
)
)



)