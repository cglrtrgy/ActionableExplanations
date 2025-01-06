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
	

(:action drop
:parameters (?x - hoist ?y - crate ?z - surface ?p - place)
:precondition
(and
( at ?z ?p )
( lifting ?x ?y )
( at ?x ?p )
( clear ?z )

)
:effect
(and
( clear ?y )
( on ?y ?z )
( available ?x )
( at ?y ?p )
(not ( lifting ?x ?y ))
(not ( clear ?z ))
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
( clear ?z )
( lifting ?x ?y )
(not ( available ?x ))
(not ( clear ?y ))
(not ( on ?y ?z ))
(not ( at ?y ?p ))
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

(:action unload
:parameters (?x - hoist ?y - crate ?z - truck ?p - place)
:precondition
(and
( in ?y ?z )
( available ?x )
( at ?z ?p )

)
:effect
(and
( lifting ?x ?y )
(not ( in ?y ?z ))
(not ( available ?x ))
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



)