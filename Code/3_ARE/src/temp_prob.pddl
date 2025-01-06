(define (problem depotprob7512)
    (:domain depot)
    (:objects crate0 - crate crate1 - crate crate2 - crate crate3 - crate depot0 - depot distributor0 - distributor distributor1 - distributor hoist0 - hoist hoist1 - hoist hoist2 - hoist pallet0 - pallet pallet1 - pallet pallet2 - pallet truck0 - truck truck1 - truck)
        (:init
(available hoist2)
(available hoist1)
(on crate0 pallet0)
(at hoist2 distributor0)
(at crate2 distributor1)
(at crate0 depot0)
(at crate1 distributor1)
(on crate3 pallet1)
(at truck0 depot0)
(clear crate3)
(available hoist0)
(on crate1 pallet2)
(at hoist0 distributor1)
(at hoist1 distributor0)
(at crate3 distributor0)
(at pallet1 distributor0)
(at hoist0 distributor0)
(at pallet2 distributor1)
(clear crate2)
(at truck1 depot0)
(at hoist0 depot0)
(on crate2 crate1)
(clear crate0)
(at pallet0 depot0)
(at hoist2 distributor1)
)
(:goal
    (and
(on crate0 pallet2)
(on crate2 pallet1)
(on crate1 crate2)
)))